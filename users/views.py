import my_settings
import bcrypt
import json
import jwt

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction

from users.models     import User
from posts.models     import Post

class SignUpView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            password = data['password']
            email    = data['email']
            nickname = data['nickname']

            if not name:
                return JsonResponse({'message':'NOT_INPUT_NAME'},status=400)

            if not password:
                return JsonResponse({'message':'NOT_INPUT_PASSWORD'},status=400)

            if not email:
                return JsonResponse({'message':'NOT_INPUT_EMAIL'},status=400)

            if not nickname:
                return JsonResponse({'message':'NOT_INPUT_NICKNAME'},status=400)

            if not my_settings.EMAIL_CHECK.match(email):
                return JsonResponse({'message':'INVALID_EMAIL'},status=400)
            
            if not my_settings.PASSWORD.match(password):
                return JsonResponse({'message':'INVALID_PASSWORD'},status=400)

            hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                name     = name,
                password = hashed_pw,
                email    = email,
                nickname = nickname,
            )
            return JsonResponse({'message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            password = data['password']
            email    = User.objects.filter(email=data['email']).first()

            if not email:
                return JsonResponse({'message':'INVALID_ID_ERROR'},status=401)
            
            if not bcrypt.checkpw(password.encode('utf-8'), email.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PW_ERROR'},status=401)
            
            encoded_jwt = jwt.encode({'user id': email.id}, my_settings.SECRET_KEY, algorithm = my_settings.ALGORITHM)
            return JsonResponse({'message':encoded_jwt}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)