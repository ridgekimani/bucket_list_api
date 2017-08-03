import json

import unittest

from app import app, app_config

from app.models import User

app.config.from_object(app_config['testing'])


class TestRegisterApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register_user(self):
        data = dict(email='test@email.com', password='test_password')
        response = self.app.post('/auth/register', data=data, content_type='application/json')
        print(response)
        self.assertTrue(response.status_code, 200)

    def test_register_with_existing_details(self):
        data = dict(email='test@user.com', password='test_password')
        response = self.app.post('/auth/register', data=json.dumps(data))
        self.assertTrue(response.status_code, 409)

    def test_register_with_missing_details(self):
        data = dict(email='test@email2.com')
        response = self.app.post('/auth/register/', data=json.dumps(data))
        self.assertTrue(response.status_code, 400)
        response = self.app.post('/auth/register?password=test_password')
        self.assertTrue(response.status_code, 300)

    def test_register_with_invalid_email(self):
        data = dict(email='test.email.com')
        response = self.app.post('/auth/register', data=json.dumps(data))
        self.assertTrue(response.status_code, 401)

    def tearDown(self):
        User.drop_all()


class TestLoginApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login_user(self):
        data = dict(email='test@user.com', password='test_password')
        response = self.app.post('/auth/login', data=json.dumps(data))
        print (response.status_code)
        self.assertTrue(response.status_code, 200)

    def test_login_user_with_invalid_credentials(self):
        data = dict(email='test@email.com', password='test_passwor')
        response = self.app.post('/auth/login', data=json.dumps(data))
        self.assertTrue(response.status_code, 401)
        data = dict(email='test@emaill.com', password='test_password')
        response = self.app.post('/auth/login', data=json.dumps(data))
        self.assertTrue(response.status_code, 400)

    def test_login_with_less_credentials(self):
        response = self.app.post('/auth/login')
        self.assertTrue(response.status_code, 400)
        data = dict(password='password')
        response = self.app.post('/auth/login', data=json.dumps(data))
        self.assertTrue(response.status_code, 400)


class TestResetPassword(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_reset_email(self):
        data = dict(email='test@email.com')
        response = self.app.post('/auth/reset_password', data=json.dumps(data))
        self.assertTrue(response.status_code, 201)

    def test_reset_non_existing_email(self):
        data = dict(email='testing@email.com')
        response = self.app.post('/auth/reset_password', data=json.dumps(data))
        self.assertTrue(response.status_code, 400)

    def test_reset_email_with_less_credentials(self):
        response = self.app.post('/auth/reset_password')
        self.assertTrue(response.status_code, 400)


class TestDeleteAccount(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_delete_account(self):
        data = dict(email='test@email.com')
        response = self.app.post('/auth/delete_account', data=data)
        self.assertTrue(response.status_code, 200)

    def test_delete_with_an_non_existing_account(self):
        data = dict(email='test@test.test')
        response = self.app.post('/auth/delete_account', data=data)
        self.assertTrue(response.status_code, 400)
