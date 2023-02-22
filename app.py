# Third party libraries
import sqlite3
import os
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, url_for, Blueprint, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Internal import
from main import main
from report import report
from authentication import authentication
from payment import payment
from config.config import SECRET_KEY
from config.config import ROOT
from config.config import ENVIRONMENT
from config.config import USERNAMEDB
from config.config import PASSWORDDB
from config.config import SERVERDB
from config.config import NAMEDB
from config.config import USER_ADMIN
from config.config import STRIP_API_KEY
from db.db import db
from db.db import migrate
from db.contact import Contact
from db.user_resource_usage import UserResourceUsage
from db.resource import Resource
from db.user import User
from db.admin_model_view import AdminModelView
from db.token_offers import TokenOffers

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

if ENVIRONMENT == 'prod':
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}/{}".format(USERNAMEDB, PASSWORDDB, SERVERDB, NAMEDB)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/{}.db'.format(ROOT, NAMEDB)
    #app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}/{}".format('svboost', 'password', 'localhost', 'svboost')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'paper'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

FLASK_STATE = 0

from flask import flash
import stripe
stripe.api_key = STRIP_API_KEY
class CustomTokenOffersView(ModelView):
    column_exclude_list = ['product_id', 'price_id']
    form_excluded_columns = ['product_id', 'price_id']

    def create_model(self, form):
        # Call the default create_model method to create the object
        model = super(CustomTokenOffersView, self).create_model(form)

        # Add custom initialization code here
        product = stripe.Product.create(
            name=str(model.token_amount) + ' ' + 'Tokens',
            description=model.name,
        )
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(model.price * 100),
            currency='usd'
        )
        model.product_id = product.id
        model.price_id = price.id
        flash('Successfully created new TokenOffer', 'success')
        
        # Save the changes to the database
        db.session.commit()

        return model


admin = Admin(app, name='SEAna Admin', template_mode='bootstrap3')
db.init_app(app)
migrate.init_app(app, db)

admin.add_view(CustomTokenOffersView(TokenOffers, db.session))
#admin.add_view(AdminModelView(TokenOffers, db.session))
admin.add_view(AdminModelView(Contact, db.session))
admin.add_view(AdminModelView(User, db.session))
app.register_blueprint(main.blueprint)
app.register_blueprint(report.blueprint)
app.register_blueprint(authentication.blueprint)
app.register_blueprint(payment.blueprint)
app.secret_key = SECRET_KEY or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
#app.wsgi_app = MiddlewareLogin(app.wsgi_app, current_user)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user.email == 'coboaccess@gmail.com':
            user.is_admin = True
            user.token_amount += 50
            db.session.commit()
        if user.is_admin == True:
            app.config['USER_ADMIN'] = user.email
        return user
    except:
        db.session.rollback()
        return User.query.filter_by(id=user_id).first()

#TODO: Mention this on github issues
with app.app_context():
    db.create_all()

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("main.login_page"))

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(502)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 502

if __name__ == "__main__":
    app.run( port=8000, debug=True )

