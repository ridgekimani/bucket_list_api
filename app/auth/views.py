import uuid

from app.models import User

from flask import Blueprint, request, jsonify, make_response

from flask.views import MethodView

from validate_email import validate_email

auth = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterApi(MethodView):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address')), 400)

        if not validate_email(email) or len(email) < 5:
            return make_response(jsonify(dict(error='Invalid email address')), 400)

        if not password:
            return make_response(jsonify(dict(error='Please enter your password')), 400)

        if len(password) < 6:
            return make_response(jsonify(dict(error='Your password must be 6 characters long')),
                                 400)

        if User.exists(email=email):
            return make_response(jsonify(dict(error='A user exists with that email')), 409)

        user = User(email=email, password=password).save()

        return make_response(jsonify(dict(user=user.email)), 200)


class LoginApi(MethodView):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address!')), 400)

        if not password:
            return make_response(jsonify(dict(error='Please enter your password!')), 400)

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(jsonify(dict(error='Email not found! Please register to '
                                                    'continue')), 400)

        if not user.check_password(password):
            return make_response(jsonify(dict(error='Incorrect password!')), 403)

        return make_response(jsonify(dict(email=user.email, password=str(user.password))), 200)


class LogoutApi(MethodView):
    def post(self):
        pass


class ResetPassword(MethodView):
    def post(self):
        email = request.form.get('email')

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address')), 400)

        if not User.exists(email=email):
            return make_response(jsonify(dict(error='Email not found!')), 400)

        password = str(uuid.uuid4())[:8]

        user = User.query.filter_by(email=email).first()
        user.password = password
        user.save()

        return make_response(dict(success='New generated password is sent. Please make sure you '
                                          'change!'), 201)


class ChangePassword(MethodView):
    def post(self):
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()

        if not user.check_password(old_password):
            return make_response(jsonify(dict(error='Incorrect password!')), 403)

        if len(new_password) < 6:
            return make_response(jsonify(dict(error='Your password must be 6 characters long')),
                                 400)

        if new_password == confirm_new:
            return make_response(jsonify(dict(error='Passwords do not match!')), 400)

        user.password = new_password
        user.save()
        return make_response(jsonify(dict(success='Password changed successfully')), 200)

auth.add_url_rule('/register', view_func=RegisterApi.as_view('register-api'))
auth.add_url_rule('/login', view_func=LoginApi.as_view('login-api'))
auth.add_url_rule('/logout', view_func=LogoutApi.as_view('logout-api'))
auth.add_url_rule('/reset_password', view_func=ResetPassword.as_view('reset-api'))
auth.add_url_rule('/change_password', view_func=ChangePassword.as_view('change_password-api'))
