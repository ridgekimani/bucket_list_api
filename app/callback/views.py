
from app.utils import login_required
from flask import make_response, jsonify, Blueprint
from flask.views import MethodView

callback = Blueprint('callback', __name__, url_prefix='/api/v1/')


class CallBack(MethodView):
    @login_required
    def post(self):
        return make_response(jsonify({"Success": "Authorized"}), 200)

    @login_required
    def get(self):
        return make_response(jsonify({"Success": "Authorized"}), 200)


callback.add_url_rule('callback', view_func=CallBack.as_view('callback'))
