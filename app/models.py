import datetime

from app import app

from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy, BaseQuery

from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType

db = SQLAlchemy(app)
hashing = Bcrypt(app)
make_searchable()


class BucketQuery(BaseQuery, SearchQueryMixin):
    """
    Query class mixin for making search for the bucket
    """
    pass


class ItemQuery(BaseQuery, SearchQueryMixin):
    """
    Query class mixin for making item related searches
    """
    pass


class User(db.Model):
    """
    This class contains tables that will be used by the user
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column(db.LargeBinary(), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.now())
    is_active = db.Column(db.Boolean(), default=True)
    last_login = db.Column(db.DateTime(), nullable=True)
    buckets = db.relationship("Bucket", backref='user', lazy='dynamic',
                              cascade="delete, delete-orphan")
    activities = db.relationship("Activity", backref='user', lazy='dynamic',
                                 cascade="delete, delete-orphan")

    @hybrid_property
    def password(self):
        """
        A getter for the password
        :return: password
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Used to set the password
        :param password:
        :return: hashed password
        """
        self._password = hashing.generate_password_hash(password)

    def check_password(self, password):
        """
        Used to confirm a user's password
        :param password:
        :return: bool
        """
        return hashing.check_password_hash(self.password, password)

    @staticmethod
    def exists(email):
        """
        Used to check if the user exists in the database
        :param email:
        :return: bool
        """
        user = User.query.filter_by(email=email).first()
        return True if user else False

    def save(self):
        """
        Used to save User instances to the db
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return User.query.filter_by(email=self.email).first()

    @classmethod
    def drop_all(cls):
        """
        Used to drop all the data for the User table
        :return:
        """
        try:
            db.session.query(cls).delete()
            db.session.commit()

        except Exception:
            db.session.rollback()

    def get_id(self):
        """
        Used to get the user id
        :return: user id
        """
        return self.user_id

    def generate_token(self):
        """
        Used for generating a token for authentication
        :return:
        """
        key = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        return key.dumps(dict(id=self.id))

    @classmethod
    def verify_token(cls, token):
        """
        Used to verify the validity of a token
        :param token:
        :return: None or user id
        """
        key = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])

        try:
            data = key.loads(token)

        except (SignatureExpired, BadSignature):
            return None
        return cls.query.filter_by(id=data['id']).first()

    @staticmethod
    def delete(email):
        """
        Used to delete a user
        :param email:
        """
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()

    def get_or_create(self):
        if User.exists(self.email):
            return User.query.filter_by(email=self.email).first()

        return self.save()


class Bucket(db.Model):
    """
    This contains tables for the bucket
    """
    __tablename__ = 'bucket'
    query_class = BucketQuery

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_name = db.Column(db.String(70), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created = db.Column(db.DateTime(), default=datetime.datetime.now())
    updated = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100), nullable=False)
    activities = db.relationship("Activity", backref='bucket', lazy='dynamic',
                                 cascade="delete, delete-orphan")
    search_vector = db.Column(TSVectorType('bucket_name', 'description'))

    def get_id(self):
        """
        Used to get the specific id for a bucket
        :return: bucket_id
        """
        return self.bucket_id

    def save(self):
        """
        Used to save the bucket
        :return: bucket instance
        """
        db.session.add(self)
        db.session.commit()
        return Bucket.query.filter_by(id=self.id).first()

    @staticmethod
    def delete(bucket_id, user):
        """
        Used to delete a bucket
        :param bucket_id:
        :param user:
        """
        bucket = Bucket.query.filter_by(id=bucket_id, user_id=user).first()
        db.session.delete(bucket)
        db.session.commit()

    @property
    def serialize(self):
        """
        Returns a serialized object of the bucket
        :return: serialized obj
        """
        serialized_obj = dict(id=self.id, bucket_name=self.bucket_name,
                              created=str(self.created.date()), user=self.user.email,
                              description=self.description, updated=str(self.updated))
        return serialized_obj

    @staticmethod
    def exists(bucket_id, user_id):
        """
        Check if a bucket exists using it's name
        :param bucket_id:
        :param user_id:
        :return: bool
        """

        bucket = Bucket.query.filter_by(id=bucket_id, user_id=user_id).first()
        return True if bucket else False

    @staticmethod
    def test_duplicate(bucket_name, user):
        """
        Tests duplicate of the bucket name
        :param bucket_name:
        :param user:
        :return: bool
        """
        bucket = Bucket.query.filter_by(bucket_name=bucket_name, user_id=user).first()
        return True if bucket else False


class Category(db.Model):
    """
    Used when adding bucket, to give more description
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(70), nullable=False, unique=True)
    category = db.relationship(Bucket, backref='category', lazy='dynamic')

    def save(self):
        """
        Used to save the category
        :return: category instance
        """
        db.session.add(self)
        db.session.commit()
        return Category.query.filter_by(id=self.id).first()

    @staticmethod
    def exists(category_name):
        """
        Checks the existence of a category and get or create
        :param category_name:
        :return: category instance
        """
        category = Category.query.filter_by(category_name=category_name).first()
        return category if category else Category(category_name=category_name).save()


class Activity(db.Model):
    """
    Table containing activity related data
    """
    __tablename__ = 'activity'
    query_class = ItemQuery

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text())
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime(), default=datetime.datetime.now())
    updated = db.Column(db.DateTime(), default=datetime.datetime.now())
    search_vector = db.Column(TSVectorType('description'))

    def get_id(self):
        return self.id

    def save(self):
        """
        Used to save data to the current session
        :return: Activity instance
        """
        db.session.add(self)
        db.session.commit()
        return Activity.query.filter_by(id=self.id).first()

    @property
    def serialize(self):
        """
        Returns a serialized object of the Item
        :return: serialized obj
        """
        serialized_obj = dict(activity_id=self.id, description=self.description,
                              user=self.user.email, created=str(self.created.date()),
                              bucket_id=self.bucket.id, updated=str(self.updated.date()))
        return serialized_obj

    @staticmethod
    def exists(bucket_id, user_id, activity_id):
        """
        Used to check if a bucket exists
        :param bucket_id:
        :param user_id:
        :param activity_id:
        :return: bool
        """
        activity = Activity.query.filter_by(bucket_id=bucket_id, user_id=user_id,
                                            id=activity_id).first()
        return True if activity else False

    @staticmethod
    def delete(bucket_id, activity_id, user_id):
        """
        Used to delete an activity
        :param bucket_id:
        :param activity_id:
        :param user_id:
        """
        activity = Activity.query.filter_by(bucket_id=bucket_id, user_id=user_id,
                                            id=activity_id).first()
        db.session.delete(activity)
        db.session.commit()

    @staticmethod
    def test_duplicate(bucket_id, user_id, description):
        """
        Tests duplicate of the description
        :param bucket_id:
        :param user_id:
        :param description
        :return: bool
        """
        activity = Activity.query.filter_by(bucket_id=bucket_id, user_id=user_id,
                                            description=description).first()
        return True if activity else False
