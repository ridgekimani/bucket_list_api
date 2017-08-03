from flask import Flask

from settings.settings import app_config

app = Flask(__name__)

TESTING = True

if TESTING:
    app.config.from_object(app_config['testing'])
else:
    app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlist


app.register_blueprint(auth)
app.register_blueprint(bucketlist)
