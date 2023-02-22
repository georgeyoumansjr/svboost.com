from flask_login import UserMixin
from config.config import STRIPE_PRODUCT_ID
from .db import db

import stripe

class TokenOffers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    token_amount = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    price_id = db.Column(db.String(150), unique=False, nullable=True)
    product_id = db.Column(db.String(150), unique=False, nullable=True)

        


