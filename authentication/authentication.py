# Python standard libraries
import json
import sqlite3
import re
import uuid
import hashlib

# Third party libraries
from flask import redirect, request, url_for, Blueprint, render_template, jsonify, make_response, session, make_response
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from config.config import GOOGLE_CLIENT_ID
from config.config import GOOGLE_CLIENT_SECRET
from config.config import GOOGLE_DISCOVERY_URL
from config.config import USER_ADMIN
from config.config import PASSWORD_ADMIN
from db.user import User
from db.db import db
from main.main import templates_path as general_template_path
from config.config import ROOT

from email.mime.text import MIMEText
import google_auth_oauthlib.flow
from flask import request, redirect, session, url_for
import os, sys
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import binascii

from main.email_utility import send_email_helper
import calendar
import datetime
import time

import codecs

blueprint = Blueprint('authentication', __name__,
                      template_folder='../',
                      static_url_path='/static',
                      static_folder='../static')

templates_path = "authentication/templates/"

# --------------------------------------------
# ---------------- PROFILE -------------------
# --------------------------------------------

@blueprint.route("/profile", methods=['GET'])
def profile():
    return render_template(templates_path+"authentication/profile.html")


# --------------------------------------------
# ---------------- LOGIN -------------------
# --------------------------------------------

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@blueprint.route("/google/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@blueprint.route("/google/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
        #
        #check before creating a new user at each login
    try:
        user = User.query.filter_by(email=users_email).first()

        if not user:
            user = User(
                id=unique_id, name=users_name, email=users_email, password=None, profile_pic=picture, is_active=True
            )
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        try:
            user = User.query.filter_by(email=users_email).first()

            if not user:
                user = User(
                    id=unique_id, name=users_name, email=users_email, password=None, profile_pic=picture, is_active=True
            )
            db.session.add(user)
            db.session.commit()
        except:
            print("\n\n>>>>>>>>>> An exception was raised when trying to get the user from the database:")
            print(str(e))
            user = None

    # Begin user session by logging the user in
    if user.password == None:
        login_user(user)
    else:
        return redirect(url_for("main.login_page", message="User with same email already registered"))

    # Send user back to homepage
    resp = make_response(redirect(url_for("main.index")))
    resp.set_cookie('usersession', 'content', 600)
    return resp

@blueprint.route("/facebook/login/callback")
def facebook_callback():
    return redirect(url_for("main.index"))

@blueprint.route("/facebook/login")
def facebook_login():
    data = request.args['data']
    data = json.loads(data)
    unique_id = data['id']
    users_name = data['name']
    users_email = data['email']

    user = User.query.filter_by(id=unique_id).first()
    if not user:
        user = User(
            id=unique_id, name=users_name, email=users_email, password=None, profile_pic='', is_active=True
        )
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    return url_for("main.index")

@blueprint.route("/seana/login", methods=['POST'])
def own_login():
    email = request.form.get("email")
    password = request.form.get("password")
    warning = {}

    email_admin = USER_ADMIN
    password_admin = PASSWORD_ADMIN
    if email != None and password != None:
        #email_is_valid, password_is_valid = validate_email_and_pwd(email, password)
        if email == email_admin:
            if password == password_admin:
                user = User.query.filter_by(email=email).first()
                if not user:
                    user = User(
                        id="useradmin2021", name="admin", email=email_admin, password=password_admin, profile_pic='', is_active = True, is_admin = True
                    )

                    db.session.add(user)
                    db.session.commit()

                    login_user(user)
                    resp = make_response(redirect(url_for("main.index")))
                    resp.set_cookie('usersession', 'content', 600)
                    return resp

                login_user(user)
                resp = make_response(redirect(url_for("main.index")))
                resp.set_cookie('usersession', 'content', 600)
                return resp

    if email != None and password != None:
        email_is_valid, password_is_valid = validate_email_and_pwd(email, password)
        if email_is_valid and password_is_valid:
            user = User.query.filter_by(email=email).first()
            if user:
                md5_obj = hashlib.md5(password.encode())
                password = md5_obj.hexdigest()
                if password == user.password:
                    if user.is_active:
                        login_user(user)
                    else:
                        return redirect(url_for("main.login_page", message="Account is not verified"))

                    resp = make_response(redirect(url_for("main.index")))
                    resp.set_cookie('usersession', 'content', 600)
                    return resp

    return redirect(url_for("main.login_page",  message='Email or password not valid'))

@blueprint.route("/seana/register", methods=['POST'])
def own_register():
    unique_id = str(uuid.uuid1())
    user_name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    retyped_password = request.form.get("retyped_password")
    warning = {}

    if email != None and password != None and user_name != None and password == retyped_password:
        email_is_valid, password_is_valid = validate_email_and_pwd(email, password)
        if email_is_valid["is_valid"] and password_is_valid["is_valid"]:
            md5_obj = hashlib.md5(password.encode())
            password = md5_obj.hexdigest()

            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    id=unique_id, name=user_name, email=email, password=password, profile_pic='', is_active=False
                )
                code, timestamp = send_confirm_email(user, url_for('authentication.confirm_email', _external=True), "confirmation_email.html")
                user.token = code
                user.expiry = timestamp

                db.session.add(user)
                db.session.commit()

                return redirect(url_for("main.login_page", message='You were registered with success. A verification link was sent to your email to confirm your account.'));

            else:
                return redirect(url_for("main.register_page", message='There is already an account registered with chosen email'));

        if email_is_valid["is_valid"] == False and password_is_valid["is_valid"] == False:
            return redirect(url_for("main.register_page", message= 'Email and password are invalid. ' + email_is_valid["message"] + '. ' + password_is_valid["message"]));
        elif not password_is_valid["is_valid"]:
            return redirect(url_for("main.register_page", message= 'Password is invalid. ' + password_is_valid["message"] ));
        elif not email_is_valid["is_valid"]:
            return redirect(url_for("main.register_page", message= password_is_valid["message"]));

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("HTTP_COOKIE", None);
    return redirect(url_for("main.landing_page"))

@blueprint.route('/callbackforsetupmail', methods=['GET'])
def callbackforsetupmail():
    global FLASK_STATE
    state = FLASK_STATE

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        ROOT + '/credentials.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        state=state)
    flow.redirect_uri = url_for('authentication.callbackforsetupmail', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials

    with open(ROOT + '/token.json', 'w') as token:
        token.write(credentials.to_json())

    return "done"

@blueprint.route('/setupmail', methods=['POST'])
def setup_mail():
    if request.form['username'] == USER_ADMIN and request.form['password'] == PASSWORD_ADMIN:

        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            ROOT + '/credentials.json',
            scopes=['https://www.googleapis.com/auth/gmail.send'])

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = url_for('authentication.callbackforsetupmail', _external=True)

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
            prompt='consent')
        global FLASK_STATE
        FLASK_STATE = state

        return authorization_url + "\n"

@blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    if request.form['email']:
        user = User.query.filter_by(email=request.form['email']).first()


        if user:

            if user.password != None:

                code = binascii.hexlify(os.urandom(20)).decode()
                link = url_for('authentication.confirm_reset_code', _external=True) + "?code=" + code
                msg = codecs.open(ROOT+"/main/email/reset_password_email.html", 'r').read()

                msg = msg.replace("$1", link)
                msg = msg.replace("$2", url_for('main.contact_page', _external=True))

                send_email_helper(subject='Password Reset', message_body=msg, to=user.email)

                current_datetime = datetime.datetime.utcnow()
                future_datetime = current_datetime + datetime.timedelta(minutes=5)
                future_timetuple = future_datetime.timetuple()
                future_timestamp = calendar.timegm(future_timetuple)

                user.token = code
                user.expiry = future_timestamp
                db.session.commit()

                return redirect(url_for("main.login_page", message="Reset link sent to your email"))

            else:
                return redirect(url_for("main.login_page", message="It is not possible to reset password for a social login account"))

        else:
            return redirect(url_for("main.login_page", message="Email is not related to any user"))

    return redirect(url_for("main.login_page", message="It was not possible to proceed"))


def send_confirm_email(user, url, tpl):
    code = binascii.hexlify(os.urandom(20)).decode()
    link = url + "?code=" + code
    msg = codecs.open(ROOT+"/main/email/{}".format(tpl), 'r').read()

    msg = msg.replace("$1", link)
    msg = msg.replace("$2", url_for('main.contact_page', _external=True))

    send_email_helper(subject='Confirmation E-mail', message_body=msg, to=user.email)

    current_datetime = datetime.datetime.utcnow()
    future_datetime = current_datetime + datetime.timedelta(minutes=30)
    future_timetuple = future_datetime.timetuple()
    future_timestamp = calendar.timegm(future_timetuple)

    return code, future_timestamp


@blueprint.route('/confirm-email', methods=['get'])
def confirm_email():
    user = ''
    if request.args['code']:
        print(">> Request has confirmation code")
        try:
            user = User.query.filter_by(token=request.args['code']).first()
            print(">> User was retrieved with success from db")
        except Exception as e:
            print(">> An exception was raised. Error {}".format(str(e)))

        if user:
            if user.password != 'None':
                print(">> User has password")

                ts_now = calendar.timegm(time.gmtime())

                if str(user.expiry) > str(ts_now):
                    print(">> Confirmation code hasn't expired")
                    user.is_active = True
                    db.session.commit()
                    return redirect(url_for("main.login_page", message="Account confirmed with success."))

                print(">> Confirmation code has expired")

                return redirect(url_for("main.login_page", message="Link may have expired."))

            print(">> Cannot confirm the email for this user - Third party user")
            return redirect(url_for("main.login_page", message=" Cannot confirm the email for this user - Third party user"))

        print(">> Link is invalid")
        return redirect(url_for("main.login_page", message="Invalid link"))

    print(">> Invalid request")
    return redirect(url_for("main.login_page", message="Invalid request"))

@blueprint.route('/confirm-reset-code', methods=['get'])
def confirm_reset_code():
    if request.args['code']:
        print(">> Request has confirmation code")
        try:
            user = User.query.filter_by(token=request.args['code']).first()
            print(">> User was found by using confirmation code")
        except Exception as e:
            print(">> An exception was raised. Error {}".format(str(e)))
            user = None

        if user:
            if user.password != 'None':
                print(">> User has password")

                ts_now = calendar.timegm(time.gmtime())
                if str(user.expiry) > str(ts_now):
                    #redirect to inset new password
                    print(">> Confirmation code hasn't expired")
                    return redirect(url_for("main.new_password_page", code=request.args['code']))

                print(">> Confirmation code has expired")
                return redirect(url_for("main.login_page", message="Link may have expired - try the reset password again."))

            print(">> Cannot reset password for this user - Third party user")
            return redirect(url_for("main.login_page", message="Cannot reset password for this user - Third party user"))

        print(">> Link is invalid")
        return redirect(url_for("main.login_page", message="Invalid link"))

    print(">> Invalid request")
    return redirect(url_for("main.login_page", message="Invalid request"))

@blueprint.route('/update-password', methods=['post'])
def update_password():
    if request.form['pwd'] == request.form['repeatedpwd']:
        user = User.query.filter_by(token=request.form['code']).first()
        if user:
            if user.password != 'None':
                md5_obj = hashlib.md5(request.form['pwd'].encode())
                password = md5_obj.hexdigest()
                user.password = password
                db.session.commit()

                return redirect(url_for("main.login_page", message="Password updated"))

    return redirect(url_for("main.login_page", message="Problem during password reset"))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def validate_email_and_pwd(email, password):
    return email_validator(email), password_validator(password);

def email_validator(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if re.search(regex,email):
        return { "is_valid": True, "message" : "Email is valid"}
    else:
        return { "is_valid": False, "message" : "Email is not valid"}

def password_validator(passwd):
    SpecialSym =['$', '@', '#', '%', '.']
    val = True
    msg = "Password is valid"

    if len(passwd) < 6:
        msg = 'length should be at least 6'
        val = False

    if len(passwd) > 20:
        msg = 'length should be not be greater than 20'
        val = False

    if not any(char.isdigit() for char in passwd):
        msg = 'Password should have at least one numeral'
        val = False

    if not any(char in SpecialSym for char in passwd):
        msg = 'Password should have at least one of the symbols $@#.'
        val = False

    return { "is_valid": val, "message": msg}

def setCookie(user):
    res = make_response('cookie')
    res.set_cookie('sv', user, max_age=60*60*2)
    return res
