from app.models import User

from flask import Blueprint, request, jsonify, make_response

from flask.views import MethodView

auth = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterApi(MethodView):
    def post(self):
        email = request.args.get('email')
        password = request.args.get('password')

        if not email:
            return make_response(jsonify({'error': 'Please enter your email address'}), 400)

        if not password:
            return make_response(jsonify({'error': 'Please enter your password'}), 400)

        if User.exists(email=email):
            return make_response(jsonify({'error': 'A user exists with that email'}), 409)

        user = User(email=email, password=password)

        return make_response(jsonify(dict(user=user.email, password=user.password)), 200)


class LoginApi(MethodView):
    def post(self):
        email = request.args.get('email')
        password = request.args.get('password')

        if not email:
            return make_response(jsonify({'error': 'Please enter your email address!'}), 400)

        if not password:
            return make_response(jsonify({'error': 'Please enter your password!'}), 400)

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(jsonify({'error': 'Email not found! Please register to '
                                                   'continue'}), 400)

        if not user.check_password(password):
            return make_response(jsonify({'error': 'Incorrect password!'}))

        return make_response(jsonify(dict(email=user.email, password=str(user.password))), 200)


auth.add_url_rule('/register', view_func=RegisterApi.as_view('register-api'))
auth.add_url_rule('/login', view_func=LoginApi.as_view('login-api'))
