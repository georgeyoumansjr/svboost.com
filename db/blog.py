from .db import db
from datetime import date

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    text = db.Column(db.String(350), unique=False, nullable=True)
    publish_date = db.Column(db.Date, unique=False, default=date.today)
