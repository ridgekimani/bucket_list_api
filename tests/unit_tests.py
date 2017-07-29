from unittest import TestCase

from app import app, app_config

app.config.from_object(app_config['testing'])


class TestRegisterApi(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register_user(self):
        data = dict(username='test_username', password='test_password')
        response = self.app.post('/auth/register')