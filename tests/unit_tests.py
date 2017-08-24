import json

import unittest

from app import app, app_config

from app.models import db, User, Bucket, Activity

app.config.from_object(app_config['testing'])


class TestRegisterApi(unittest.TestCase):
    """
    Test for Register User endpoint
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='test@users.com', password='test_password').get_or_create()

    def test_register_user(self):
        data = dict(email='test@user1.com', password='test_password1', confirm_password='test_password1')
        response = self.app.post('/api/v1/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 200

    def test_register_with_existing_details(self):
        data = dict(email='test@users.com', password='test_password', confirm_password='test_password')
        response = self.app.post('/api/v1/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 409

    def test_register_with_invalid_details(self):
        data = dict(email='test@email2.com')
        response = self.app.post('/api/v1/auth/register', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                 data=json.dumps(dict(password='test_password', confirm_password='sd')))
        assert response.status_code == 400
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                 data=json.dumps(dict(
                                     email='test@email2.com',
                                     password='test',
                                     confirm_password='test')
                                 ))
        assert response.status_code == 400

    def test_register_with_invalid_email(self):
        data = dict(email='test.email.com')
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                 data=json.dumps(data))
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestLoginApi(unittest.TestCase):
    """
    Test for login user endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='test@users.com', password='test_password').get_or_create()

    def test_login_user(self):
        data = dict(email='test@users.com', password='test_password')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(data),
                                 content_type='application/json')

        assert response.status_code == 200

    def test_login_user_with_invalid_credentials(self):
        data = dict(email='test@email.com', password='test_passwor')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

        data = dict(email='test@users.com', password='test_passwor')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 403

    def test_login_with_less_credentials(self):
        response = self.app.post('/api/v1/auth/login', content_type='application/json')
        assert response.status_code == 400

        data = dict(password='password')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestResetPassword(unittest.TestCase):
    """
    Test for reset password endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        User(email='ridgekimani@yahoo.com', password='test_password').get_or_create()

    def test_reset_email(self):
        data = dict(email='ridgekimani@yahoo.com')
        response = self.app.post('/api/v1/auth/reset_password', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 201

    def test_reset_non_existing_email(self):
        data = dict(email='testing@email.com')
        response = self.app.post('/api/v1/auth/reset_password', data=json.dumps(data),
                                 content_type='application/json')
        assert response.status_code == 400

    def test_reset_email_with_less_credentials(self):
        response = self.app.post('/api/v1/auth/reset_password', content_type='application/json')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestChangePassword(unittest.TestCase):
    """
    Test for change password endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@user.com', password='test_password').save()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email

    def test_change_password(self):
        data = json.dumps(dict(old_password='test_password', new_password='password',
                               confirm_password='password'))
        res = self.app.put('/api/v1/auth/change_password', data=data,
                           content_type='application/json')
        assert res.status_code == 200

    def test_with_invalid_initial_password(self):
        data = json.dumps(dict(old_password='test_pass', new_password='password',
                               confirm_password='password'))
        res = self.app.put('/api/v1/auth/change_password', data=data,
                           content_type='application/json')
        assert res.status_code == 403

    def test_with_missing_details(self):
        data = json.dumps(dict(old_password='test_password', new_password='password'))
        res = self.app.put('/api/v1/auth/change_password', data=data,
                           content_type='application/json')
        assert res.status_code == 400
        data = json.dumps(dict(old_password='test_password', confirm_password='password'))
        res = self.app.put('/api/v1/auth/change_password', data=data,
                           content_type='application/json')
        assert res.status_code == 400

    def test_password_validators(self):
        data = json.dumps(dict(old_password='test_password', new_password='pass',
                               confirm_password='pass'))
        res = self.app.put('/api/v1/auth/change_password', data=data,
                           content_type='application/json')
        assert res.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestDeleteAccount(unittest.TestCase):
    """
    Test delete account endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@email.com', password='test_password').get_or_create()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email

    def test_delete_account(self):
        data = json.dumps(dict(password='test_password'))
        response = self.app.delete('/api/v1/auth/delete_account', data=data,
                                   content_type='application/json')
        assert response.status_code == 200

    def test_delete_account_with_wrong_credentials(self):
        data = json.dumps(dict(password='test_pass'))
        response = self.app.delete('/api/v1/auth/delete_account',
                                   content_type='application/json', data=data)
        assert response.status_code == 403

    def test_delete_account_with_no_data(self):
        response = self.app.delete('/api/v1/auth/delete_account', content_type='application/json')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestBucketListTestCases(unittest.TestCase):
    """
    Test bucket list test cases
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        user = User(email='test@email.com', password='test_password').get_or_create()
        self.bucket = Bucket(bucket_name='Test', user=user, description='Test').save()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = user.email

    def test_create_bucket(self):
        data = json.dumps(dict(bucket_name='test_bucket', description='test_description'))

        response = self.app.post('/api/v1/bucketlists/', data=data, content_type='application/json')
        assert response.status_code == 201
        response2 = self.app.post('/api/v1/bucketlists/', data=data, content_type='application/json')
        assert response2.status_code == 409

    def test_view_buckets(self):
        response = self.app.get('/api/v1/bucketlists/')
        assert response.status_code == 200

    def test_view_buckets_with_id(self):
        response = self.app.get('/api/v1/bucketlists/' + str(self.bucket.id))
        assert response.status_code == 200

    def test_view_buckets_with_limits(self):
        response = self.app.get('/api/v1/bucketlists/?page=1&limit=1')
        assert response.status_code == 200

    def test_view_buckets_with_invalid_limits(self):
        response = self.app.get('/api/v1/bucketlists/?page=one&limit=one')
        assert response.status_code == 400

    def test_update_bucket(self):
        Bucket(bucket_name='test1', user_id=self.bucket.user_id, description='test desc').save()
        data = json.dumps(dict(bucket_name='update test bucket', category='Update Category',
                               description='test update'))

        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 200

        data2 = json.dumps(dict(bucket_name='test1', category='Update Category',
                                description='test update'))

        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id), data=data2,
                                content_type='application/json')
        print(response.status_code)
        assert response.status_code == 409

    def test_update_bucket_without_id(self):
        data = json.dumps(dict(bucket_name='update test bucket',
                               description='test update description'))
        response = self.app.put('/api/v1/bucketlists/', data=data, content_type='application/json')
        assert response.status_code == 400

    def test_bucket_with_no_bucket_name(self):
        data = json.dumps(dict(description='test update description'))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 400

    def test_bucket_with_no_description(self):
        data = json.dumps(dict(bucket_name='update test bucket'))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 200

    def test_post_bucket_with_invalid_content(self):
        data = json.dumps(dict(bucket_name='  '))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id), data=data,
                                content_type='application/json')
        assert response.status_code == 400
        response2 = self.app.post('/api/v1/bucketlists/', data=data, content_type='application/json')
        assert response2.status_code == 400

    def test_update_bucket_with_invalid_bucket(self):
        data = json.dumps(dict(bucket_name='update test bucket',
                               description='test update description'))
        response = self.app.put('/api/v1/bucketlists/0', data=data, content_type='application/json')
        assert response.status_code == 400

    def test_delete_bucket(self):
        response = self.app.delete('/api/v1/bucketlists/' + str(self.bucket.id))
        assert response.status_code == 200
        response1 = self.app.delete('/api/v1/bucketlists/' + str(self.bucket.id))
        assert response1.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestItemTestCases(unittest.TestCase):
    """
    Test Item test cases
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.user = User(email='test@email.com', password='test_password').get_or_create()
        self.bucket = Bucket(bucket_name='Test', user_id=self.user.id, description='Test').save()

        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = self.user.email

    def test_add_activity(self):
        data = json.dumps(dict(description='test_description'))
        response = self.app.post('/api/v1/bucketlists/' + str(self.bucket.id) + '/items',
                                 data=data, content_type='application/json')

        assert response.status_code == 201

        response2 = self.app.post('/api/v1/bucketlists/' + str(self.bucket.id) + '/items',
                                  data=data, content_type='application/json')

        assert response2.status_code == 409

    def test_add_activity_with_no_data(self):
        response = self.app.post('/api/v1/bucketlists/' + str(self.bucket.id) + '/items',
                                 content_type='application/json')
        assert response.status_code == 400

    def test_get_activities(self):
        response = self.app.get('/api/v1/bucketlists/' + str(self.bucket.id) + '/items',
                                content_type='application/json')
        assert response.status_code == 200

    def test_get_specific_activity(self):
        act = Activity(description='Test desc', user=self.user, bucket_id=self.bucket.id).save()
        response = self.app.get('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json')
        assert response.status_code == 200

    def test_get_activities_with_limits(self):
        response = self.app.get('/api/v1/bucketlists/' + str(self.bucket.id)
                                + '/items' + '?page=1&limit=1', content_type='application/json')
        assert response.status_code == 200

    def test_update_activity(self):
        act = Activity(description='Test desc', user=self.user, bucket_id=self.bucket.id).save()
        Activity(description='test1', user=self.user, bucket_id=self.bucket.id).save()
        data = json.dumps(dict(description='Update description'))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json', data=data)
        assert response.status_code == 200
        data = json.dumps(dict(description='test1'))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json', data=data)
        assert response.status_code == 409

    def test_update_activity_with_no_description(self):
        act = Activity(description='Test desc', user=self.user, bucket_id=self.bucket.id).save()
        data = json.dumps(dict(x='y'))
        response = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json', data=data)
        assert response.status_code == 400

        response2 = self.app.put('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json', data=json.dumps(dict(description='  ')))
        assert response2.status_code == 400

    def test_delete_activity(self):
        act = Activity(description='Test desc', user=self.user, bucket_id=self.bucket.id).save()
        response = self.app.delete('/api/v1/bucketlists/' + str(self.bucket.id) + '/items/' + str(
            act.id), content_type='application/json')
        assert response.status_code == 200

    def test_post_activity_with_invalid_content(self):
        data = json.dumps(dict(description='  '))
        response = self.app.post('/api/v1/bucketlists/' + str(self.bucket.id) + '/items',
                                 data=data, content_type='application/json')

        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


class TestSearchApi(unittest.TestCase):
    """
    Test search api
    """
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.user = User(email='test@email.com', password='test_password').get_or_create()
        self.bucket = Bucket(bucket_name='Test', user_id=self.user.id, description='Test').save()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = self.user.email

    def test_search(self):
        Activity(description='Test desc', user=self.user, bucket_id=self.bucket.id).save()
        response = self.app.get('/api/v1/search?q=test')
        assert response.status_code == 200

    def test_search_with_no_parameters(self):
        response = self.app.get('/api/v1/search')
        assert response.status_code == 400

    def tearDown(self):
        User.drop_all()
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
