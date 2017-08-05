from app.models import Bucket, Activity
from flask import Blueprint, make_response, jsonify, request


search = Blueprint('search', __name__, url_prefix='/search')


# TODO improve the search logic
@search.route('/', methods=['GET'])
def search_api():
    query = request.args.get('q')
    if not query:
        return make_response(jsonify(error='Please enter search parameters'), 400)

    bucket_lists = Bucket.query.filter_by(bucket_name=query).all()
    activities = Activity.query.filter_by(description=query).all()
    bucket_obj = [bucket.serialize for bucket in bucket_lists]
    activity_obj = [activity.serialize for activity in activities]
    return make_response(jsonify(buckets=bucket_obj, activities=activity_obj))
