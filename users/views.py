import my_settings
import bcrypt
import json

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction

from users.models     import User
from admins.models    import Admin

class UserpostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            nickname  = data['nickname']
            password  = data['password']
            content   = data['content']
            title     = data['title']
            secret_is = data.get('secret_is',False)
            tag       = data.get('tag',None)

            if not nickname:
                return JsonResponse({'message':'NOT_INPUT_NICKNAME'},status=400)

            if not content:
                return JsonResponse({'message':'NOT_INPUT_CONTENT'},status=400)

            if not title:
                return JsonResponse({'message':'NOT_INPUT_TITLE'},status=400)

            if not my_settings.PASSWORD.match(password):
                return JsonResponse({'message':'INVALID_PASSWORD'},status=400)

            hash_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                nickname  = nickname,
                password  = hash_pw,
                content   = content,
                title     = title,
                secret_is = secret_is,
                tag       = tag
            )
            return JsonResponse({'message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

    def get(self,request):
        posts = User.objects.all().order_by('pk')
        answer = [{
            'no'           : post.pk,
            'nickname'     : post.nickname,
            'title'        : post.title,
            'content'      : post.content,
            'hits'         : post.hits,
            'created_at'   : post.created_at,
            'secret_is'    : post.secret_is,
            'tag'          : post.tag,
            'admin_asnwer' : {
                            'no'               : Admin.objects.get(user_post_id=post).pk,
                            'admin_title'      : Admin.objects.get(user_post_id=post).title,
                            'admin_content'    : Admin.objects.get(user_post_id=post).content,
                            'admin_hits'       : Admin.objects.get(user_post_id=post).hits,
                            'admin_created_at' : Admin.objects.get(user_post_id=post).created_at } if post.admin_is_answer else None
        }for post in posts ]

        return JsonResponse({'data' : answer},status=200)