import datetime

from app import app

from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property


db = SQLAlchemy(app)
hashing = Bcrypt(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column(db.LargeBinary(), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.now())
    is_active = db.Column(db.Boolean(), default=True)
    last_login = db.Column(db.DateTime(), nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = hashing.generate_password_hash(password)

    def check_password(self, password):
        return hashing.check_password_hash(self.password, password)

    @staticmethod
    def exists(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.user_id


class Bucket(db.Model):
    __tablename__ = 'bucket'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_name = db.Column(db.String(70), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_by = db.Column(db.DateTime(), default=datetime.datetime.now())
    description = db.Column(db.String(100), nullable=False)
    activities = db.relationship("Activity", back_populates="bucket")

    def get_id(self):
        return self.bucket_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(70), nullable=False, unique=True)
    category = db.relationship(Bucket)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text())
    bucket_id_ = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    bucket = db.relationship("Bucket", back_populates="activities")
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_id(self):
        return self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
