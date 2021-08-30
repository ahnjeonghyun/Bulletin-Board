import jwt
import my_settings

from users.models         import User

from django.http.response import JsonResponse

def login_required(func):
     def decorator(self, request, *args, **kwargs):
        try:
            access_token  = request.headers['Authorization']
            decoded_token = jwt.decode(access_token, my_settings.SECRET_KEY, algorithms=my_settings.ALGORITHM)

            user = User.objects.get(id=decoded_token['user id'])
            
            request.user = user
            return func(self, request)

        except User.DoesNotExist:
            return JsonResponse({'message':'UNKNOWN_USER'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
            
        return decorator

