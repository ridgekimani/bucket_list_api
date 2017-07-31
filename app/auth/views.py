import uuid

from app.models import User

from app.utils import validate_email, send_mail

from flask import Blueprint, request, jsonify, make_response, session, abort

from flask.views import MethodView


auth = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterApi(MethodView):

    def post(self):
        if not request.json:
            abort(400)

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address')), 400)

        if not validate_email(email):
            return make_response(jsonify(dict(error='Invalid email address')), 400)

        if not password:
            return make_response(jsonify(dict(error='Please enter your password')), 400)

        if len(password) < 6:
            return make_response(jsonify(dict(error='Your password must be 6 characters long')),
                                 400)

        if User.exists(email=email):
            return make_response(jsonify(dict(error='A user exists with that email')), 409)

        user = User(email=email, password=password).save()

        token = user.generate_token()
        session['token'] = token
        session['user'] = user.email

        return make_response(jsonify(dict(user=user.email, token=token.decode('ascii'))), 200)


class LoginApi(MethodView):
    def post(self):

        if not request.json:
            abort(400)

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

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

        token = user.generate_token()
        session['token'] = token
        session['user'] = user.email
        return make_response(jsonify(dict(email=user.email, token=token.decode())), 200)


class LogoutApi(MethodView):
    def post(self):
        session.pop('user', None)
        session.pop('token', None)
        return make_response(jsonify(dict(success='Logout successful')), 200)


class ResetPassword(MethodView):
    def post(self):
        if not request.json:
            abort(400)

        data = request.get_json()
        email = data.get('email')

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address')), 400)

        if not User.exists(email=email):
            return make_response(jsonify(dict(error='Email not found!')), 400)

        password = str(uuid.uuid4())[:8]

        user = User.query.filter_by(email=email).first()
        status = send_mail(email, password)

        if not status:
            return make_response(jsonify(dict(error='Password was not reset. Please try resetting '
                                                    'it again')), 500)
        user.password = password
        user.save()

        return make_response(jsonify(dict(success='An email has been sent with instructions for '
                                                  'your new password')), 201)


class ChangePassword(MethodView):
    def post(self):
        if not request.json:
            abort(400)

        data = request.get_json()
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new = data.get('confirm_password')

        if not old_password:
            return make_response(jsonify(dict(error='Please enter your old password')), 400)

        if not any([confirm_new, new_password]):
            return make_response(jsonify(dict(error='Please enter and confirm your new '
                                                    'password')), 400)

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(jsonify(dict(error='Email does not exist!')), 400)

        if not user.check_password(old_password):
            return make_response(jsonify(dict(error='Incorrect password!')), 403)

        if new_password != confirm_new:
            return make_response(jsonify(dict(error='Passwords do not match!')), 400)

        if len(new_password) < 6:
            return make_response(jsonify(dict(error='Your password must be more than 6 characters '
                                                    'long')), 400)

        user.password = new_password
        user.save()
        return make_response(jsonify(dict(success='Password changed successfully')), 200)


auth.add_url_rule('/register', view_func=RegisterApi.as_view('register-api'))
auth.add_url_rule('/login', view_func=LoginApi.as_view('login-api'))
auth.add_url_rule('/logout', view_func=LogoutApi.as_view('logout-api'))
auth.add_url_rule('/reset_password', view_func=ResetPassword.as_view('reset-api'))
auth.add_url_rule('/change_password', view_func=ChangePassword.as_view('change_password-api'))
