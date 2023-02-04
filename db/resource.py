from flask_login import UserMixin

from .db import db

class Resource(db.Model):
	id = db.Column(db.String(90), primary_key=True)
	name = db.Column(db.String(90), unique=False, nullable=False)
	#urusages = db.relationship('UserResourceUsage', backref='resource', lazy=True)


