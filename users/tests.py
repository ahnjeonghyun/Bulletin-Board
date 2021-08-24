import json
import unittest
import my_settings
import jwt

from django.test       import Client, TestCase

from unittest.mock     import patch, MagicMock, Mock
from users.models      import User
from posts.models      import Post

class UserSignUpTest(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_user_sign_up_success(self):
        body = {
            "name"     : "안정현",
            "password" : "wkdwkdaos123!",
            "email"    : "tgrf3090@gmail.com",
            "nickname" : "안사장"
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'SUCCESS' , status_code=201)

    def test_user_sign_up_name_fail(self):
        body = {
            "name"     : "",
            "password" : "wkdwkdaos123!",
            "email"    : "tgrf3090@gmail.com",
            "nickname" : "안사장"
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'NOT_INPUT_NAME' , status_code=400)
    
    def test_user_sign_up_nickname_fail(self):
        body = {
            "name"     : "안정현",
            "password" : "wkdwkdaos123!",
            "email"    : "tgrf3090@gmail.com",
            "nickname" : ""
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'NOT_INPUT_NICKNAME' , status_code=400)

    def test_user_sign_up_password_fail(self):
        body = {
            "name"     : "안정현",
            "password" : "wwdsa",
            "email"    : "tgrf3090@gmail.com",
            "nickname" : "안사장"
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'INVALID_PASSWORD' , status_code=400)
    
    def test_user_sign_up_email_fail(self):
        body = {
            "name"     : "안정현",
            "password" : "wwdsa2123!",
            "email"    : "tgrf3090gmail.com",
            "nickname" : "안사장"
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'INVALID_EMAIL' , status_code=400)

    def test_user_sign_up_key_error_fail(self):
        body = {
            
            "password" : "wwdsa2123!",
            "email"    : "tgrf3090gmail.com",
            "nickname" : "안사장"
        }

        response = self.client.post('/users/sign-up', json.dumps(body), content_type='application/json')
        self.assertContains(response, 'KEY_ERROR' , status_code=400)

class UserSignInTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(
        name      = "안정현",
        password  = "$2b$12$MMkiJR.xORQG7SvNoNgUieTKPW4h2RtbIIRiN8rlRAOscgeMY2h7.",
        email     = "tgrf3090@gmail.com",
        nickname  = "tgrf07"
        )
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_user_login_success(self):
        body = {
            "password" : "wjdgus123!",
            "email"    : "tgrf3090@gmail.com"
            }

        encoded_jwt = jwt.encode({'user id': User.objects.get(email=body['email']).pk}, my_settings.SECRET_KEY, algorithm = my_settings.ALGORITHM)

        response = self.client.post('/users/sign-in', json.dumps(body), content_type='application/json')
        self.assertContains(response, encoded_jwt, status_code = 200)

    def test_user_login_email_fail(self):
        body = {
            "password" : "wjdgus123!",
            "email"    : "tgrf3090@gmail.co"
        }

        response = self.client.post('/users/sign-in', json.dumps(body), content_type='application/json')
        self.assertContains(response, "INVALID_ID_ERROR", status_code = 401)
    
    def test_user_login_password_fail(self):
        body = {
            "password" : "wjdgus123",
            "email"    : "tgrf3090@gmail.com"
        }

        response = self.client.post('/users/sign-in', json.dumps(body), content_type='application/json')
        self.assertContains(response, "INVALID_PW_ERROR", status_code = 401)
