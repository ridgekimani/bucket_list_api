import json

import unittest

from app import app, app_config

from app.models import db, User, Bucket

app.config.from_object(app_config['testing'])


class TestRegisterApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='test@users.com', password='test_password').get_or_create()

    def test_register_user(self):
        data = dict(email='test@user1.com', password='test_password1')
        response = self.app.post('/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 201

    def test_register_with_existing_details(self):
        data = dict(email='test@users.com', password='test_password')
        response = self.app.post('/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 409

    def test_register_with_missing_details(self):
        data = dict(email='test@email2.com')
        response = self.app.post('/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400
        response = self.app.post('/auth/register', content_type='application/json',
                                 data=json.dumps(dict(password='test_password')))
        assert response.status_code == 400

    def test_register_with_invalid_email(self):
        data = dict(email='test.email.com')
        response = self.app.post('/auth/register', content_type='application/json',
                                 data=json.dumps(data))
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestLoginApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='test@users.com', password='test_password').get_or_create()

    def test_login_user(self):
        data = dict(email='test@users.com', password='test_password')
        response = self.app.post('/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 200

    def test_login_user_with_invalid_credentials(self):
        data = dict(email='test@email.com', password='test_passwor')
        response = self.app.post('/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

        data = dict(email='test@users.com', password='test_passwor')
        response = self.app.post('/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 403

    def test_login_with_less_credentials(self):
        response = self.app.post('/auth/login', content_type='application/json')
        assert response.status_code == 400

        data = dict(password='password')
        response = self.app.post('/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestResetPassword(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='ridge.kimani@andela.com', password='test_password').get_or_create()

    def test_reset_email(self):
        data = dict(email='ridge.kimani@andela.com')
        response = self.app.post('/auth/reset_password', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 201

    def test_reset_non_existing_email(self):
        data = dict(email='testing@email.com')
        response = self.app.post('/auth/reset_password', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

    def test_reset_email_with_less_credentials(self):
        response = self.app.post('/auth/reset_password', content_type='application/json')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestChangePassword(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@user.com', password='test_password').save()
        token = user.generate_token()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email
                sess['token'] = token

    def test_change_password(self):
        data = json.dumps(dict(old_password='test_password', new_password='password',
                               confirm_password='password'))
        res = self.app.post('/auth/change_password', data=data, content_type='application/json')
        assert res.status_code == 200

    def test_with_invalid_initial_password(self):
        data = json.dumps(dict(old_password='test_pass', new_password='password',
                               confirm_password='password'))
        res = self.app.post('/auth/change_password', data=data, content_type='application/json')
        assert res.status_code == 403

    def test_with_missing_details(self):
        data = json.dumps(dict(old_password='test_password', new_password='password'))
        res = self.app.post('/auth/change_password', data=data, content_type='application/json')
        assert res.status_code == 400
        data = json.dumps(dict(old_password='test_password', confirm_password='password'))
        res = self.app.post('/auth/change_password', data=data, content_type='application/json')
        assert res.status_code == 400

    def test_password_validators(self):
        data = json.dumps(dict(old_password='test_password', new_password='pass',
                               confirm_password='pass'))
        res = self.app.post('/auth/change_password', data=data, content_type='application/json')
        assert res.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestDeleteAccount(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@email.com', password='test_password').get_or_create()
        token = user.generate_token()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email
                sess['token'] = token

    def test_delete_account(self):
        response = self.app.delete('/auth/delete_account')
        assert response.status_code == 200

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestBucketListTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@email.com', password='test_password').get_or_create()
        self.bucket = Bucket(bucket_name='Test', user=user, description='Test').save()
        token = user.generate_token()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email
                sess['token'] = token

    def test_create_bucket(self):
        data = json.dumps(dict(bucket_name='test_bucket', description='test_description'))

        response = self.app.post('/bucketlists/', data=data, content_type='application/json')
        assert response.status_code == 201

    def test_view_buckets(self):
        response = self.app.get('/bucketlists/')
        assert response.status_code == 200

    def test_view_buckets_with_id(self):
        response = self.app.get('/bucketlists/' + str(self.bucket.id))
        assert response.status_code == 200

    def test_view_buckets_with_limits(self):
        response = self.app.get('/bucketlists/?page=1&limit=1')
        assert response.status_code == 200

    def test_view_buckets_with_invalid_limits(self):
        response = self.app.get('/bucketlists/?page=one&limit=one')
        assert response.status_code == 400

    def test_update_bucket(self):
        data = json.dumps(dict(bucket_name='update test bucket', category='Update Category',
                               description='test update'))

        response = self.app.put('/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 200

    def test_update_bucket_without_id(self):
        data = json.dumps(dict(bucket_name='update test bucket',
                               description='test update description'))
        response = self.app.put('/bucketlists/', data=data, content_type='application/json')
        assert response.status_code == 400

    def test_bucket_with_no_bucket_name(self):
        data = json.dumps(dict(description='test update description'))
        response = self.app.put('/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 400

    def test_bucket_with_no_description(self):
        data = json.dumps(dict(bucket_name='update test bucket'))
        response = self.app.put('/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 400

    def test_update_bucket_with_invalid_bucket(self):
        data = json.dumps(dict(bucket_name='update test bucket',
                               description='test update description'))
        response = self.app.put('/bucketlists/0', data=data, content_type='application/json')
        assert response.status_code == 400

    def test_delete_bucket(self):
        response = self.app.delete('/bucketlists/' + str(self.bucket.id))
        assert response.status_code == 200
        response1 = self.app.delete('/bucketlists/' + str(self.bucket.id))
        assert response1.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestItemActivityTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_activity(self):
        pass

    def test_get_activities(self):
        pass

    def test_get_specific_activity(self):
        pass

    def test_get_activity_with_limits(self):
        pass

    def test_update_activity(self):
        pass

    def test_delete_activity(self):
        pass


if __name__ == '__main__':
    unittest.main()
