from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


def get_time():
    return int(time())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    password_hold = db.Column(db.String(128))

    # Relationships - children
    preferences = db.relationship('Preference', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password, *option):
        if not option:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hold = generate_password_hash(password)
            self.password_hash = 'waiting'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        token = jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
        return token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    img = db.Column(db.String(128))
    link = db.Column(db.String(128))
    description = db.Column(db.String(512))

    # Relationships - parents
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Relationships - children
    preferences = db.relationship('Preference',
                                  backref='thing',
                                  lazy='dynamic')

    def __repr__(self):
        return '<Thing {}: {}>'.format(self.id, self.title)


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128))
    created_at = db.Column(db.Integer, default=get_time)

    # Relationships - parents
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thing_id = db.Column(db.Integer, db.ForeignKey('thing.id'))

    def __repr__(self):
        return '<Preference {}>'.format(self.id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    # Relationships - children
    things = db.relationship('Thing', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}: {}>'.format(self.id, self.title)
