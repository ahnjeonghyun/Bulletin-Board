import json
import unittest
import my_settings

from django.test       import Client, TestCase

from unittest.mock     import patch, MagicMock, Mock
from users.models      import User
from admins.models     import Admin

class UserpostTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def tearDown(self):
        User.objects.all().delete()

    def test_post_non_secret_success(self):
        body = {
            "nickname"  : "김떡순",
            "password"  : "asd1234!",
            "content"   : "가입했습니다",
            "title"     : "제목",
            "secret_is" : False,
            "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'SUCCESS', status_code=201)

    def test_post_secret_success(self):
        body = {
            "nickname"  : "김떡순",
            "password"  : "asd1234!",
            "content"   : "가입했습니다",
            "title"     : "제목",
            "secret_is" : True,
            "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'SUCCESS', status_code=201)

    def test_post_invalid_pw_fail(self):
        body = {
            "nickname"  : "김떡순",
            "password"  : "111111111",
            "content"   : "가입했습니다",
            "title"     : "제목",
            "secret_is" : True,
            "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'INVALID_PASSWORD', status_code=400)
    
    def test_post_not_input_nickname_fail(self):
        body = {
        "nickname"  : "",
        "password"  : "",
        "content"   : "가입했습니다",
        "title"     : "제목",
        "secret_is" : True,
        "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'NOT_INPUT_NICKNAME', status_code=400)
    
    def test_post_not_input_content_fail(self):
        body = {
        "nickname"  : "김떡순",
        "password"  : "",
        "content"   : "",
        "title"     : "제목",
        "secret_is" : True,
        "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'NOT_INPUT_CONTENT', status_code=400)

    def test_post_not_input_title_fail(self):
        body = {
        "nickname"  : "김떡순",
        "password"  : "",
        "content"   : "내용",
        "title"     : "",
        "secret_is" : True,
        "tag"       : "가입,완료"
        }

        response = self.client.post('/users/posts', json.dumps(body), content_type = 'application/json')
        self.assertContains(response, 'NOT_INPUT_TITLE', status_code=400)

class UserpostgetTest(TestCase):
    @patch('django.utils.timezone.now', return_value='2021-08-10T13:47:06.522Z')
    def setUp(self, mock_date):
        self.client = Client()
        User.objects.create(
            pk              = 1,
            nickname        = '김밥',
            password        = 'pw1234!',
            content         = '내용',
            title           = '제목',
            secret_is       = True,
            tag             = None,
            admin_is_answer = True,
            )

        Admin.objects.create(
            user_post_id = User.objects.get(pk=1).id,
            content      = '답변내용',
            title        = '답변제목',
        )
        self.assertEqual.__self__.maxDiff = None

    def tearDown(self):
        User.objects.all().delete()
        Admin.objects.all().delete()

    def test_get_posting(self):
        response = self.client.get('/users/posts')
        self.assertEqual(response.json(),
                {"data": [{
                        "no": 1,
                        "nickname": "김밥",
                        "title": "제목",
                        "content": "내용",
                        "hits": 0,
                        "created_at": '2021-08-10T13:47:06.522Z',
                        "secret_is": True,
                        "tag": None,
                        "admin_asnwer": {
                            "no": 1,
                            "admin_title": "답변제목",
                            "admin_content": "답변내용",
                            "admin_hits": 0,
                            "admin_created_at":'2021-08-10T13:47:06.522Z' 
                            }
                        }
                    ]
                }
            )
        self.assertEqual(response.status_code, 200)