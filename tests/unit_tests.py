from unittest import TestCase

from app import app, app_config

from app.models import User

app.config.from_object(app_config['testing'])


class TestRegisterApi(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register_user(self):
        response = self.app.post('/auth/register?email=test@emaill.com&password=test_password')
        print (response)

    def tearDown(self):
        User.drop_all()


