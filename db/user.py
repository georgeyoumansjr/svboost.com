from flask_login import UserMixin

from .db import db

class User(db.Model, UserMixin):
    id = db.Column(db.String(90), primary_key=True)
    name = db.Column(db.String(90), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=True)
    profile_pic = db.Column(db.String(90), unique=False, nullable=True)
    stripe_session = db.Column(db.String(200), unique=True, nullable=True)
    token = db.Column(db.String(200), unique=True, nullable=True)
    expiry = db.Column(db.String(100), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, unique=False, nullable=True)
    status = db.Column(db.Integer, unique=False, nullable=True, default=1)
    urusages = db.relationship('UserResourceUsage', backref='user', lazy=False)
    is_admin = db.Column(db.Boolean, unique=False, nullable=True)
    token_amount = db.Column(db.Integer, nullable=True, default=25)
