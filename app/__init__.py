from flask import Flask, make_response, jsonify

from settings.settings import app_config

app = Flask(__name__)

app.config.from_object(app_config['development'])

from app.auth.views import auth
from app.bucketlists.views import bucketlist
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


app.register_blueprint(auth)
app.register_blueprint(bucketlist)
app.register_blueprint(search)
