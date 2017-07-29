from flask import Flask

from settings.settings import app_config

app = Flask(__name__)

app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlists


app.register_blueprint(bucketlists)
app.register_blueprint(auth)
