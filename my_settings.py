SECRET_KEY = 'django-insecure-ebc385gmwbt1s*22u$5b&i6x9ie+!d8#v6)#kboe^^4vc^)nh)'

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'YJH_bread',
        'USER': 'root',
        'PASSWORD': 'wjdgus123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

ALGORITHM = 'HS256'