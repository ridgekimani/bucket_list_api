from unittest import TestCase

from app import app, app_config

from app.models import User

app.config.from_object(app_config['testing'])


class TestRegisterApi(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register_user(self):
        response = self.app.post('/auth/register?email=test@emaill.com&password=test_password')
        self.assertTrue(response.status_code, 200)

    def test_register_with_existing_details(self):
        response = self.app.post('/auth/register?email=test@email.com&password=test_password')
        self.assertTrue(response.status_code, 409)

    def test_register_with_missing_details(self):
        response = self.app.post('/auth/register?email=testemail2.com')
        self.assertTrue(response.status_code, 400)
        response = self.app.post('/auth/register?password=test_password')
        self.assertTrue(response.status_code, 400)

    def test_register_with_invalid_email(self):
        response = self.app.post('/auth/register?email=test')
        self.assertTrue(response.status_code, 400)

    # def tearDown(self):
    #     User.drop_all()


class TestLoginApi(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login_user(self):
        response = self.app.post('/auth/login?email=test@email.com&password=test_password')
        self.assertTrue(response.status_code, 200)

    def test_login_user_with_invalid_credentials(self):
        response = self.app.post('/auth/login?email=test@email.com&password=password')
        self.assertTrue(response.status_code, 401)
        response = self.app.post('/auth/login?email=test@emails.com&password=test_password')
        self.assertTrue(response.status_code, 400)

    def test_login_with_less_credentials(self):
        response = self.app.post('/auth/login')
        self.assertTrue(response.status_code, 400)
        response = self.app.post('/auth/login?password=password')
        self.assertTrue(response.status_code, 400)
