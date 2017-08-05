import re

from flask import session, make_response, jsonify, request

from app.models import User

from functools import wraps

from smtplib import SMTP, SMTPException


def validate_email(email):
    if len(email) > 7:
        if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                    email) is not None:
            return True
    return False


def send_mail(recipient, password):
    sender = 'betatestmail10@gmail.com'
    pwd = 'naivasha'
    message = "Your new password is %s" % password
    try:
        server = SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(sender, recipient, message)
        server.close()
        return True

    except SMTPException:
        return False


def login_required(func):
    @wraps(func)
    def check_login_status(*args, **kwargs):
        if 'token' in request.headers or 'user' in session:
            email = session.get('user')
            token = request.headers.get('token')
            if token and not email:
                if User.verify_token(token):
                    session['user'] = User.verify_token(token).email
                else:
                    return make_response(jsonify(dict(error='Invalid session. Please login')), 403)

            if email and not token:
                User.query.filter_by(email=email).first()
        else:
            return make_response(jsonify(error='Unauthorised. Please login'), 403)
        return func(*args, **kwargs)
    return check_login_status
