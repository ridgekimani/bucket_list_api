from app.utils import login_required

from flask import Blueprint
from flask.views import MethodView

bucketlist = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


class BucketListsApi(MethodView):
    @login_required
    def get(self, bucket_id=None):
        pass

    @login_required
    def post(self):
        pass

    @login_required
    def put(self, bucket_id):
        pass

    @login_required
    def delete(self, bucket_id):
        pass


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
