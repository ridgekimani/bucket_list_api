from app.models import Bucket, Activity, User, Category

from app.utils import login_required, validate_text

from datetime import datetime

from flask import Blueprint, session, make_response, jsonify, request
from flask.views import MethodView

bucketlist = Blueprint('bucketlists', __name__, url_prefix='/api/v1/bucketlists')


class BucketListsApi(MethodView):
    """
    This class is used to handle the bucket list operations that will be done by a user
    This includes create, delete, update and read buckets
    """

    @login_required
    def get(self, bucket_id=None):
        """
        Used to get the buckets that have been added
        :param bucket_id:
        :return: serialized objects or list of serialized objects
        """
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
            next_page = request.base_url + '?page=' + str(page+1) + '&limit=' + str(limit)

        if page_buckets.has_prev:
            previous_page = request.base_url + '?page=' + str(page-1) + '&limit=' + str(limit)

        return make_response(jsonify(buckets=[bucket.serialize for bucket in page_buckets.items],
                                     next_page=next_page, previous_page=previous_page))

    @login_required
    def post(self):
        """
        Used to add a user's bucket
        :return: serialized bucket
        """

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

        if not validate_text(bucket_name):
            return make_response(jsonify(dict(error="Please enter a valid bucket name")), 400)

        if not validate_text(description):
            return make_response(jsonify(dict(error="Please enter a valid description")), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()

        if Bucket.test_duplicate(bucket_name, user.id):
            return make_response(jsonify(error='Bucket name exists. Add activities from it'), 409)

        data = dict(bucket_name=bucket_name, user_id=user.id, category_id=category.id,
                    description=description)
        bucket = Bucket(**data).save()
        return make_response(jsonify(bucket=bucket.serialize), 201)

    @login_required
    def put(self, bucket_id=None):
        """
        Used to update a bucket
        :param bucket_id:
        :return: serialized bucket
        """
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

        if not validate_text(bucket_name):
            return make_response(jsonify(dict(error="Please enter a valid bucket name")), 400)

        email = session.get('user')
        user = User.query.filter_by(email=email).first()
        bucket = Bucket.query.filter_by(id=bucket_id, user_id=user.id).first()

        if bucket.bucket_name != bucket_name:
            if Bucket.test_duplicate(bucket_name, user.id):
                return make_response(jsonify(dict(error="Bucket name already exists!")), 409)
            pass

        if not bucket:
            return make_response(jsonify(dict(error='Bucket not found!')), 400)

        if category:
            if not validate_text(category):
                return make_response(jsonify(dict(error="Please enter a valid description")), 400)
            category = Category.exists(category)
            bucket.category_id = category.id

        if description:
            if not validate_text(description):
                return make_response(jsonify(dict(error="Please enter a valid description")), 400)
            bucket.description = description

        bucket.bucket_name = bucket_name
        bucket.updated = datetime.now()
        bucket.save()
        return make_response(jsonify(bucket=bucket.serialize), 200)

    @login_required
    def delete(self, bucket_id=None):
        """
        Used to delete a bucket
        :param bucket_id:
        :return: serialized list of buckets
        """
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
    """
    This classs is used to perform the CRUD operations of the Items.
    This include Create, Delete, Update and Read
    The user must be logged in to consume this endpoints
    """
    @login_required
    def get(self, bucket_id=None, item_id=None):
        """
        Used to get the list of buckets or a single bucket
        :param bucket_id:
        :param item_id:
        :return: serialized bucket or serialized list of buckets
        """

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
            next_page = request.base_url + '?page=' + str(page+1) + '&limit=' + str(limit)

        if page_items.has_prev:
            previous_page = request.base_url + '?page=' + str(page-1) + '&limit=' + str(limit)

        return make_response(jsonify(buckets=[bucket.serialize for bucket in page_items.items],
                                     next_page=next_page, previous_page=previous_page))

    @login_required
    def post(self, bucket_id=None):
        """
        Used to create a single iten
        :param bucket_id:
        :return: serialized item
        """
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

        if not description:
            return make_response(jsonify(dict(error='Please describe your activity')), 400)

        if not validate_text(description):
            return make_response(jsonify(dict(error="Please enter a valid description")), 400)

        if Activity.test_duplicate(bucket_id, user.id, description):
            return make_response(jsonify(dict(error="Activity exists with the same description!")), 409)

        activity = Activity(description=description, bucket_id=bucket_id, user_id=user.id).save()
        return make_response(jsonify(dict(item=activity.serialize)), 201)

    @login_required
    def put(self, bucket_id=None, item_id=None):
        """
        Used to update the item
        :param bucket_id:
        :param item_id:
        :return: serialized item
        """
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

        if not description:
            return make_response(jsonify(dict(error='Please describe your activity')), 400)

        if not validate_text(description):
            return make_response(jsonify(dict(error="Please enter a valid description")), 400)

        activity = Activity.query.filter_by(bucket_id=bucket_id,
                                            id=item_id, user_id=user.id).first()

        if description != activity.description:
            if Activity.test_duplicate(bucket_id, user.id, description):
                return make_response(jsonify(dict(error="Item exists with that name!")), 409)

        activity.description = description
        activity.updated = datetime.now()
        activity.save()
        return make_response(jsonify(dict(item=activity.serialize)), 200)

    @login_required
    def delete(self, bucket_id, item_id):
        """
        Used to delete the item
        :param bucket_id:
        :param item_id:
        :return: available list of serialized items
        """
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
