from app.models import Bucket, Activity, User, Category

from app.utils import login_required

from datetime import datetime

from flask import Blueprint, session, make_response, jsonify, request
from flask.views import MethodView

bucketlist = Blueprint('bucketlists', __name__, url_prefix='/api/v1/bucketlists')


class BucketListsApi(MethodView):

    @login_required
    def get(self, bucket_id=None):
        limit = request.args.get('limit', None)
        page = request.args.get("page", 1)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if bucket_id:
            bucket = Bucket.query.filter_by(user=user, id=bucket_id).first()
            return make_response(jsonify(bucket=bucket.serialize), 200)

        if not all([limit, page]):
            buckets = Bucket.query.filter_by(user=user).all()
            return make_response(jsonify(buckets=[bucket_.serialize for bucket_ in buckets]), 200)

        try:
            limit = int(limit)
            page = int(page)

        except ValueError:
            return make_response(jsonify(error='Please enter valid page or limit numbers'), 400)

        page_buckets = Bucket.query.filter_by(user=user).paginate(page, limit, error_out=False)
        next_page = ''
        previous_page = ''
        if page_buckets.has_next:
            next_page = 'http://127.0.0.1:5000/bucketlists/?page=' + str(page+1) + '&limit=' + str(
                limit)

        if page_buckets.has_prev:
            previous_page = 'http://127.0.0.1:5000/bucketlists/?page=' + str(page-1) + '&limit=' \
                            + str(limit)

        return make_response(jsonify(buckets=[bucket.serialize for bucket in page_buckets.items],
                                     next_page=next_page, previous_page=previous_page))

    @login_required
    def post(self):

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        bucket_name = data.get('bucket_name')
        category = data.get('category', 'General')
        description = data.get('description')

        if not bucket_name:
            return make_response(jsonify(dict(error='Please enter the bucket name')), 400)

        category = Category.exists(category)

        if not description:
            return make_response(jsonify(dict(error='Please describe your bucket')), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        data = dict(bucket_name=bucket_name, user_id=user.id, category_id=category.id,
                    description=description)
        bucket = Bucket(**data).save()
        return make_response(jsonify(bucket=bucket.serialize), 201)

    @login_required
    def put(self, bucket_id=None):
        if not bucket_id:
            return make_response(jsonify(dict(error='Please specify the bucket id')), 400)

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        bucket_name = data.get('bucket_name')
        category = data.get('category')
        description = data.get('description')

        if not bucket_name:
            return make_response(jsonify(dict(error='Please enter the bucket name')), 400)

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
        bucket.updated = datetime.now()
        bucket.save()
        return make_response(jsonify(bucket=bucket.serialize), 200)

    @login_required
    def delete(self, bucket_id=None):
        if not bucket_id:
            return make_response(jsonify(dict(error='Please specify the bucket id')), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        if Bucket.exists(bucket_id, user.id):
            Bucket.delete(bucket_id, user.id)
            buckets = Bucket.query.filter_by(user=user).all()
            return make_response(jsonify(dict(buckets=[bucket_.serialize for bucket_ in buckets])),
                                 200)

        return make_response(jsonify(dict(error='Bucket not found!')), 400)


class ItemsApi(MethodView):

    @login_required
    def get(self, bucket_id=None, item_id=None):
        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if not bucket_id:
            return make_response(jsonify(error='Please specify your bucket id'), 400)

        if item_id and bucket_id:
            act = Activity.query.filter_by(bucket_id=bucket_id, user=user, id=item_id).first()
            return make_response(jsonify(activity=act.serialize))

        limit = request.args.get('limit')
        page = request.args.get('page', 1)

        if not all([limit, page]):
            items = Activity.query.filter_by(bucket_id=bucket_id, user=user).all()
            return make_response(jsonify(activities=[item.serialize for item in items]))

        try:
            limit = int(limit)
            page = int(page)

        except ValueError:
            return make_response(jsonify(error='Please enter valid page or limit numbers'), 400)

        page_items = Activity.query.filter_by(user=user, bucket_id=bucket_id)\
            .paginate(page, limit, error_out=False)
        next_page = ''
        previous_page = ''
        if page_items.has_next:
            next_page = 'http://127.0.0.1:5000/bucketlists/'+str(bucket_id)+'/items?page=' + \
                        str(page+1) + '&limit=' + str(limit)

        if page_items.has_prev:
            previous_page = 'http://127.0.0.1:5000/bucketlists/'+str(bucket_id)+'/items?page=' + \
                             str(page-1) + '&limit=' + str(limit)

        return make_response(jsonify(buckets=[bucket.serialize for bucket in page_items.items],
                                     next_page=next_page, previous_page=previous_page))

    @login_required
    def post(self, bucket_id=None):
        if not bucket_id:
            return make_response(jsonify(error='Please specify your bucket id'), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if not Bucket.exists(bucket_id, user.id):
            return make_response(jsonify(error='Bucket not found'), 400)

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        description = data.get('description')
        activity = Activity(description=description, bucket_id=bucket_id, user_id=user.id).save()
        return make_response(jsonify(dict(item=activity.serialize)), 201)

    @login_required
    def put(self, bucket_id=None, item_id=None):
        if not bucket_id:
            return make_response(jsonify(error='Please specify the bucket id'), 400)

        if not item_id:
            return make_response(jsonify(error='Please specify your item id'), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if not Activity.exists(bucket_id, user.id, item_id):
            return make_response(jsonify(dict(error='Activity not found')), 400)

        if not request.get_json():
            return make_response(jsonify(dict(error='Bad request. Please enter some data')), 400)

        data = request.get_json()
        description = data.get('description')
        activity = Activity.query.filter_by(bucket_id=bucket_id,
                                            id=item_id, user_id=user.id).first()
        activity.description = description
        activity.updated = datetime.now()
        activity.save()
        return make_response(jsonify(dict(item=activity.serialize)), 200)

    @login_required
    def delete(self, bucket_id, item_id):
        if not all([bucket_id, item_id]):
            return jsonify(dict(error='Please specify the bucket and the activity'), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if not Activity.exists(bucket_id, user.id, item_id):
            return make_response(jsonify(dict(error='Activity not found')), 400)

        Activity.delete(bucket_id, item_id, user.id)
        items = Activity.query.filter_by(bucket_id=bucket_id, user_id=user.id).all()
        return make_response(jsonify(items=[item.serialize for item in items]))


bucketlist.add_url_rule('/', view_func=BucketListsApi.as_view('buckets'))
bucketlist.add_url_rule('/<int:bucket_id>', view_func=BucketListsApi.as_view('bucket_specific'))
bucketlist.add_url_rule('/<int:bucket_id>/items', view_func=ItemsApi.as_view('bucket-items'))
bucketlist.add_url_rule('/<int:bucket_id>/items/<int:item_id>', view_func=ItemsApi.as_view('item'))
