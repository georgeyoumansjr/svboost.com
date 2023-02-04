from flask_login import UserMixin

from .db import db

class Contact(db.Model):
	id = db.Column(db.String(90), primary_key=True)
	name = db.Column(db.String(90), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=False, nullable=False)
	country = db.Column(db.String(90), unique=False, nullable=False)
	subject = db.Column(db.String(600), unique=False, nullable=False)
