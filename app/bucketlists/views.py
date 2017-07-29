from flask import Blueprint
from flask.views import MethodView

bucketlist = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


class BucketListsApi(MethodView):

    def get(self, bucket_id=None):
        pass

    def post(self):
        pass

    def put(self, bucket_id):
        pass

    def delete(self, bucket_id):
        pass


class ItemsApi(MethodView):
    def get(self, bucket_id):
        pass

    def post(self, bucket_id):
        pass

    def put(self, bucket_id, item_id):
        pass

    def delete(self, bucket_id, item_id):
        pass

bucketlist.add_url_rule('/', view_func=BucketListsApi.as_view('buckets'))
bucketlist.add_url_rule('/<int:bucket_id>', view_func=BucketListsApi.as_view('bucket_specific'))
bucketlist.add_url_rule('/<int:bucket_id>/items', view_func=BucketListsApi.as_view('bucket-items'))
bucketlist.add_url_rule('/<int:bucket_id>/items/<int:bucket_id>', view_func=BucketListsApi.as_view('item'))
