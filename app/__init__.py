from flask import Flask, make_response, jsonify, redirect
from flask_cors import CORS

from settings.settings import app_config

app = Flask(__name__)

CORS(app)

app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlist
from app.callback.views import callback
from app.search.views import search


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(dict(error='Resource not found')), 404)


@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify(dict(error='Server error! Please try again')), 500)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify(dict(error='Method not allowed')), 405)


@app.route('/')
def index():
    return redirect("https://app.swaggerhub.com/apis/ridgekimani/bucket_list/1.0.0")

app.register_blueprint(auth)
app.register_blueprint(bucketlist)
app.register_blueprint(callback)
app.register_blueprint(search)
