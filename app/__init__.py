from flask import Flask, make_response, jsonify

from settings.settings import app_config

app = Flask(__name__)

app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlist
from app.search.views import search


@app.errorhandler(400)
def not_found():
    return make_response(jsonify(dict(error='Resource not found')), 404)


app.register_blueprint(auth)
app.register_blueprint(bucketlist)
app.register_blueprint(search)
