import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from settings.settings import app_config

app = Flask(__name__)

TESTING = True

if TESTING:
    app.config.from_object(app_config['testing'])
else:
    app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlist
from app.search.views import search


SWAGGER_URL = '/api/docs'

API_URL = os.path.join(os.getcwd(), '/swagger/swagger.json')

swagger = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

app.register_blueprint(auth)
app.register_blueprint(bucketlist)
app.register_blueprint(search)
app.register_blueprint(swagger, url_prefix=SWAGGER_URL)
