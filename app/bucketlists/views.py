from app.utils import login_required
from app.models import Bucket, Activity, User, Category

from flask import Blueprint, session, make_response, jsonify, request
from flask.views import MethodView

bucketlist = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


class BucketListsApi(MethodView):
    @login_required
    def get(self, bucket_id=None):
        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if bucket_id:
            bucket = Bucket.query.filter_by(user=user, id=bucket_id).first()
            return make_response(jsonify(bucket=bucket.serialize), 200)

        buckets = Bucket.query.filter_by(user=user).all()
        return make_response(jsonify(buckets=[bucket_.serialize for bucket_ in buckets]), 200)

    @login_required
    def post(self):

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        bucket_name = data.get('bucket_name')
        category = data.get('category')
        description = data.get('description')

        if not bucket_name:
            return make_response(jsonify(dict(error='Please enter the bucket name')), 400)

        if not category:
            return make_response(jsonify(dict(error='Please enter the category of your bucket')),
                                 400)

        category = Category.exists(category)

        if not description:
            return make_response(jsonify(dict(error='Please describe your bucket')), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        data = dict(bucket_name=bucket_name, user_id=user.id, category_id=category.id,
                    description=description)
        bucket = Bucket(**data).save()
        return make_response(jsonify(bucket=bucket.serialize), 200)

    @login_required
    def put(self, bucket_id):
        if not bucket_id:
            return make_response(jsonify(dict(error='Please specify the bucket')), 400)

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        bucket_name = data.get('bucket_name')
        category = data.get('category')
        description = data.get('description')

        if not bucket_name:
            return make_response(jsonify(dict(error='Please enter the bucket name')), 400)

        if not category:
            return make_response(jsonify(dict(error='Please enter the category of your bucket')),
                                 400)

        if not description:
            return make_response(jsonify(dict(error='Please describe your bucket')), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        bucket = Bucket.query.filter_by(id=bucket_id, user_id=user.id).first()

        if not bucket:
            return make_response(jsonify(dict(error='Bucket not found!')), 400)

        category = Category.exists(category)
        bucket.description = description
        bucket.category_id = category.id
        bucket.bucket_name = bucket_name
        bucket.save()
        return make_response(jsonify(bucket=bucket.serialize), 200)

    @login_required
    def delete(self, bucket_id):
        if not bucket_id:
            return make_response(jsonify(dict(error='Please specify the bucket')), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        if Bucket.exists(bucket_id, user.id):
            Bucket.delete(bucket_id)
            return make_response(jsonify(dict(success='Bucket deleted successfully')), 200)

        return make_response(jsonify(dict(error='Bucket not found!')), 400)


class ItemsApi(MethodView):
    @login_required
    def get(self, bucket_id=None):
        pass

    @login_required
    def post(self, bucket_id):
        pass

    @login_required
    def put(self, bucket_id, item_id):
        pass

    @login_required
    def delete(self, bucket_id, item_id):
        pass

bucketlist.add_url_rule('/', view_func=BucketListsApi.as_view('buckets'))
bucketlist.add_url_rule('/<int:bucket_id>', view_func=BucketListsApi.as_view('bucket_specific'))
bucketlist.add_url_rule('/<int:bucket_id>/items', view_func=ItemsApi.as_view('bucket-items'))
bucketlist.add_url_rule('/<int:bucket_id>/items/<int:item_id>', view_func=ItemsApi.as_view('item'))
