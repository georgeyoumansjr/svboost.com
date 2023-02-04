from flask_login import UserMixin

from .db import db
from .user import User
from .resource import Resource

class UserResourceUsage(db.Model):
	id = db.Column(db.String(90), primary_key=True)
	resource_name = db.Column(db.String(100), unique=False, nullable=True)
	term = db.Column(db.String(90), unique=False, nullable=True)
	result = db.Column(db.String(700), unique=False, nullable=True)
	search_date = db.Column(db.String(90), unique=False, nullable=True)
	#resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=True)
	user_id = db.Column(db.String(90), db.ForeignKey('user.id'), nullable=True)
	showTour = db.Column(db.Boolean, unique=False, nullable=True, default=True)