from flask import Blueprint, request


search = Blueprint('search', __name__, url_prefix='/search')


@search.route('/', methods=['GET'])
def search_api():
    query = request.args.get('q')