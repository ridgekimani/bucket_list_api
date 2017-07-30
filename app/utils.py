import re

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
