from flask import Blueprint
from flask.views import MethodView

bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


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

# bucketlists.add_url_rule('/', BucketListsApi.as_view('buckets'))
# bucketlists.add_url_rule('/<int:bucket_id>', BucketListsApi.as_view('bucket_specific'))
# bucketlists.add_url_rule('/<int:bucket_id>/items', BucketListsApi.as_view('bucket-items'))
# bucketlists.add_url_rule('/<int:bucket_id>/items/<int:bucket_id>', BucketListsApi.as_view('item'))
