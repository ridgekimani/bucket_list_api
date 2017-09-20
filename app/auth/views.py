import uuid

from app.models import User

from app.utils import validate_email, send_mail, login_required

from flask import Blueprint, request, jsonify, make_response, session

from flask.views import MethodView


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


class RegisterApi(MethodView):
    """
    This Method view is used to Register a user
    It contains the post method only
    """
    def post(self):
        """
        Endpoint that is used to save the data to the database
        :return: json_response
        """
        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not email:
            return make_response(jsonify(dict(error='Please enter your email address')), 400)

        if not validate_email(email):
            return make_response(jsonify(dict(error='Invalid email address')), 400)

        if not password:
            return make_response(jsonify(dict(error='Please enter your password')), 400)

        if len(password) < 6:
            return make_response(jsonify(dict(error='Your password must be 6 characters long and above')),
                                 400)

        if not confirm_password:
            return make_response(jsonify(dict(error='Please confirm your password')), 400)

        if str(confirm_password) != str(password):
            return make_response(jsonify(dict(error="Passwords don't match")), 400)

        if User.exists(email=email):
            return make_response(jsonify(dict(error='A user exists with that email')), 409)

        user = User(email=email, password=password).save()

        token = user.generate_token()
        session['user'] = user.email
        response = make_response(jsonify(dict(success='Account created successfully', token=token)))
        response.headers['token'] = token
        return response


class LoginApi(MethodView):
    """
    Used to Login a user
    """

    def post(self):
        """
        Used to verify the user credentials
        :return: json response
        """
        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

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
        session['user'] = user.email
        response = make_response(jsonify(dict(success='Authenticated successfully',
                                              token=token.decode())))
        response.headers['token'] = token
        return response


class LogoutApi(MethodView):

    def post(self):
        session.pop('user', None)
        response = make_response(jsonify(dict(success='Logout successful')))
        response.headers['token'] = None
        return response


class ResetPassword(MethodView):
    """
    Used to reset a user's password when forgotten.
    It sends an email with the new auto generated password
    """

    def post(self):
        """
        Used to send details to be reset
        :return:
        """

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

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
    """
    This method is used to change the password of the user
    """

    @login_required
    def put(self):
        """
        This method is used to update the password of the user
        :return:
        """

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        email = session.get('user')
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


class DeleteAccount(MethodView):
    """
    This method is used to delete the user's account

    """

    @login_required
    def delete(self):
        """
        The user must be logged in and should provide a password to delete the account
        :return:
        """

        email = session.get('user')
        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        password = request.get_json().get('password')

        if not User.exists(email=email):
            return make_response(jsonify(dict(error='User does not exist')), 400)

        user = User.query.filter_by(email=email).first()

        if not user.check_password(password):
            return make_response(jsonify(dict(error='Incorrect password')), 403)

        User.delete(email)
        return make_response(jsonify(dict(success="Account deleted successfully")), 200)


auth.add_url_rule('/register', view_func=RegisterApi.as_view('register-api'))
auth.add_url_rule('/login', view_func=LoginApi.as_view('login-api'))
auth.add_url_rule('/logout', view_func=LogoutApi.as_view('logout-api'))
auth.add_url_rule('/reset_password', view_func=ResetPassword.as_view('reset-api'))
auth.add_url_rule('/change_password', view_func=ChangePassword.as_view('change_password-api'))
auth.add_url_rule('/delete_account', view_func=DeleteAccount.as_view('delete-account'))
