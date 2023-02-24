from flask import Blueprint, render_template, request, redirect, url_for
from flask import jsonify

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import uuid
##from .grammarcheck import check_grammar
from db.contact import Contact
from db.db import db
from db.user import User
from db.token_offers import TokenOffers
import hashlib
from .email_utility import create_message
from .email_utility import get_stored_credential
from .email_utility import build_service_message
from .email_utility import send_message
from .email_utility import send_email_helper
from config.config import EMAIL
from config.config import ROOT
import codecs
import json
from datetime import datetime
from db.user_resource_usage import UserResourceUsage
import calendar;
import time
from config.config import USER_ADMIN
from config.config import PASSWORD_ADMIN
import logging
import subprocess

blueprint = Blueprint('main', __name__,
                        template_folder='../',
                        static_url_path='/static',
                        static_folder='../static')

templates_path = "main/templates/"

DESCRIPTION_KEYWORDS = []
DESCRIPTION_INTRO = []
DESCRIPTION_BODY= []
DESCRIPTION_ENDING= []

# --------------------------------------------
# ------------------ HOME --------------------
# --------------------------------------------

@blueprint.route("/dashboard", methods=['GET'])
@login_required
def index():
    user = current_user
    tag_re = []
    key_re = []
    des_re = []
    buil_re = []

    for res in user.urusages:
        if "/search-for-tag-report" in res.resource_name:
           tag_re.append(
               {
                    "name": res.resource_name,
                    "term": res.term,
                    "result": res.result,
                    "search_date": datetime.fromtimestamp(int(res.search_date))
                }
           )

        if "/search-by-keyword" in res.resource_name:
            key_re.append(
                {
                    "name": res.resource_name,
                    "term": res.term,
                    "result": res.result,
                    "search_date": datetime.fromtimestamp(int(res.search_date))
                }
            )

        if "/search-for-description-report" in res.resource_name:
            des_re.append(
                {
                    "name": res.resource_name,
                    "term": res.term,
                    "result": res.result,
                    "search_date": datetime.fromtimestamp(int(res.search_date))
                }
            )
        if "/description-checker" in res.resource_name:
            buil_re.append(
                {
                    "name": res.resource_name,
                    "term": res.term,
                    "result": res.result,
                    "search_date": datetime.fromtimestamp(int(res.search_date))
                }
            )

    if user:
        token_amount = User.query.filter_by(id=current_user.id).first().token_amount
        return render_template(templates_path+"index.html", token_amount=token_amount, username=user.name, tag_re=reverse_filter(tag_re), key_re=reverse_filter(key_re), des_re=reverse_filter(des_re), buil_re=reverse_filter(buil_re), is_home="True")

    return ""

@blueprint.route("/search-summary/<term>", methods=['GET'])
@login_required
def search_summary(term):
    user = current_user
    terms_re = []
    term = term.replace("%20", " ")
    print(term)
    for res in user.urusages:
        print(">>> for {}".format(res.term))
        if res.term == term:
            terms_re.append(
                {
                    "name": res.resource_name,
                    "term": res.term,
                    "result": res.result.replace(",", ", ")
                }
            )


    return render_template(templates_path+"searched_term_summary.html", username=user.name, terms_re=terms_re, token_amount=token_amount)


@blueprint.route("/user", methods=['GET'])
def user_is_authorized():
    user = current_user
    if user.is_authenticated:
        return jsonify({'authenticated':True})
    return jsonify({'authenticated':False})

@blueprint.route("/", methods=['GET'])
def landing_page():
    return render_template("landing_page.html")

@blueprint.route("/register", methods=['GET'])
def register_page():
    return render_template(templates_path+"register_page.html")

@blueprint.route("/login-page", methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template(templates_path+"login_page.html")
    #arr = []
    #print(arr["index"])

@blueprint.route("/contact_page", methods=['GET'])
def contact_page():
    return render_template(templates_path+"contact_page.html")


@blueprint.route("/cart_page", methods=['GET'])
@login_required
def cart_page():
    return render_template(templates_path+"cart_page.html")

@blueprint.route("/pricing_page", methods=['GET'])
def pricing_page():
    offers = TokenOffers.query.all()
    context = []
    for offer in offers:
        context.append(offer)


    return render_template(templates_path+"pricing_page.html", offers=context)
@blueprint.route("/pricing_page/info", methods=['GET'])
def info():
    return render_template(templates_path+'info.html')


# --------------------------------------------
# ----------------- BLOGS --------------------
# --------------------------------------------
#@blueprint.route("/blogs", methods=['GET'])
#def blogs_page():
#    return render_template("blogs/blog_test.html")
@blueprint.route("/keyword-tool", methods=['GET'])
def keyword_tool_page():
    return render_template("blogs/keyword-tool/keyword-tool.html")

@blueprint.route("/keyword-tool/1", methods=['GET'])
def kwt_1():
    return render_template("blogs/keyword-tool/kwt1.html")

@blueprint.route("/us", methods=['GET'])
def us_page():
    return render_template("blogs/us/us.html")

@blueprint.route("/us/1", methods=['GET'])
def us_1():
    return render_template("blogs/us/us1.html")

@blueprint.route("/de", methods=['GET'])
def de_page():
    return render_template("blogs/de/de.html")

@blueprint.route("/de/1", methods=['GET'])
def de_1():
    return render_template("blogs/de/de1.html")


@blueprint.route("/cart", methods=['GET'])
def cart():
    return render_template(templates_path+"cart.html")

@blueprint.route("/my_account", methods=['GET'])
@login_required
def my_account():
    message = ''
    if 'message' in request.args:
        message = request.args['message']

    user = {
        "name": current_user.name,
        "email": current_user.email
    }
    if current_user.password != None:
        return render_template(templates_path+"my_account.html", user=user, editpass=True, message=message)
    else:
        return render_template(templates_path+"my_account.html", user=user, editpass=False, message=message)

@blueprint.route("/update-my-information", methods=['POST'])
@login_required
def update_my_information():
    message = 'update with success'
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    print(">>> Current password hash {}".format(password))

    newpassword = request.form.get("newpassword")
    repeatpassword = request.form.get("repeatpassword")

    try:

        user = User.query.filter_by(id=current_user.id).first()
        if user:
            user.name = name
            user.email = email
            print(">>> Current password hash {}".format(password))
            if password != "":

                md5_obj = hashlib.md5(password.encode())
                password = md5_obj.hexdigest()

                if password == user.password:
                    if newpassword == repeatpassword:
                        md5_obj = hashlib.md5(newpassword.encode())
                        newpassword = md5_obj.hexdigest()
                        user.password = newpassword
                        print(user.password)
                else:
                    message = 'current password incorrect'
            db.session.commit()
            user = {
                'name' : current_user.name,
                'email' : current_user.email
            }
            return redirect(url_for("main.my_account",  user=user, message=message))
        else:
            return redirect(url_for("main.my_account", message='problem updating the information', user=user))
    except Exception as e:
        logging.error("Exception on update_my_information. {}".format(str(e)))
        return redirect(url_for("main.my_account", message='problem updating the information', user=user))


@blueprint.route("/payment_method/<id>", methods=['GET'])
@login_required
def payment_method(id):
    user = User.query.filter_by(id=current_user.id).first()
    offer = TokenOffers.query.filter_by(id=id).first()
    return render_template(templates_path+"payment_method.html", user=user, offer=offer)

@blueprint.route("/purchase_details", methods=['GET'])
def purchase_details():
    return render_template(templates_path+"purchase_details.html")

@blueprint.route("/terms_of_service", methods=['GET'])
def terms_of_service():
    return render_template(templates_path+"terms_of_service.html")

@blueprint.route("/privacy_policy", methods=['GET'])
def privacy_policy():
    return render_template(templates_path+"privacy_policy.html")

@blueprint.route("/reset-password-page", methods=['GET'])
def reset_password_page():
    return render_template(templates_path+"reset_password_page.html")


@blueprint.route("/new-password-page", methods=['GET'])
def new_password_page():
    if request.args['code']:
        return render_template(templates_path+"new_password_page.html", code=request.args['code'])
    return render_template(templates_path+"new_password_page.html")

# --------------------------------------------
# ----------------- SEARCH -------------------
# --------------------------------------------

@blueprint.route("/search-by-video", methods=['GET'])
@login_required
def search_by_video():
    return render_template(templates_path+"search_pages/search-by-video.html")

@blueprint.route("/search-by-keyword", methods=['GET'])
@login_required
def search_by_keyword():
    return render_template(templates_path+"search_pages/search-by-keyword.html")

@blueprint.route("/search-for-tag-report", methods=['GET'])
@login_required
def search_by_keyword_in_tag():
    return render_template(templates_path+"search_pages/search-for-tag-report.html")

@blueprint.route("/search-for-description-report", methods=['GET'])
@login_required
def search_by_keyword_in_description():
    return render_template(templates_path+"search_pages/search-for-description-report.html")

@blueprint.route("/search-by-keyword-scraper", methods=['GET'])
@login_required
def search_by_keyword_scraper():
    return render_template(templates_path+"search_pages/search-by-keyword-scraper.html")

# --------------------------------------------
# ----------------- CHECKER ------------------
# --------------------------------------------
from flask import flash
@blueprint.route("/description-checker", methods=['GET'])
@login_required
def description_builder():
    user = User.query.filter_by(id=current_user.id).first()
    if user.token_amount == None or user.token_amount < 5:
        flash("You don't have enough tokens.",'error')
        return redirect('/pricing_page')
    token_amount = user.token_amount
    description_amount = int(token_amount/5)
    return render_template(templates_path+"/description_builder/description-builder.html", token_amount=token_amount, description_amount=description_amount)

@blueprint.route("/save-result", methods=['POST'])
@login_required
def save_result():
    result = request.form.getlist('result[]')
    term = request.form.getlist('term')
    resource = request.form.getlist('resource')

    try:
        result = ','.join(map(str, result))
        unique_id = str(uuid.uuid1())
        print(result)
        uru = UserResourceUsage(id=unique_id,resource_name=resource[0], term=term[0], result=result, user_id=current_user.id, search_date=calendar.timegm(time.gmtime()))
        db.session.add(uru)
        db.session.commit()
        return "Result was saved"
    except Exception as e:
        print(str(e))
        return "Something went wrong, please contact our team"

# --------------------------------------------
# ----------------- Contact ------------------
# --------------------------------------------

@blueprint.route("/send_contact", methods=['POST'])
def send_contact():
    unique_id = str(uuid.uuid1())
    name = request.form.get("name")
    email = request.form.get("email")
    country = request.form.get("country")
    subject = request.form.get("subject")
    msg = """
Name: {} <br>
email: {} <br>
country: {} <br>
## Subject <br>
{}
    """.format(name, email, country, subject)

    try:
        contact = Contact(id=unique_id,name=name,email=email,country=country,subject=subject)
        db.session.add(contact)
        db.session.commit()
        send_confirm_email(msg=msg, tpl="contact_email.html")
    except Exception as e:
        logging.error("Exception on send_contact. {}".format(str(e)))
        return redirect(url_for("main.contact_page", message='Error when submitting message'));
    return redirect(url_for("main.contact_page", message='Message submitted with success'));


@blueprint.route("/get_contact", methods=['GET'])
def get_message_contact():
    email = request.args.get("email")

    try:
        contact = Contact.get(email)
        return contact.subject
    except Exception as e:
        logging.error("Exception on get_message_contact. {}".format(str(e)))
        return redirect(url_for("main.contact_page", message='error'));

@blueprint.route("/merge-notification", methods=['POST'])
def merge_notification():
    data = request.form.getlist("payload")
    for item in data:
        item = json.loads(item)
        if ("action" in item):
            if ("closed" == item["action"]):
                if ("pull_request" in item):
                    if ("base" in item["pull_request"] and item["pull_request"]["base"]["ref"] == "master"):
                        try:
                            result = subprocess.call(ROOT+"/deploy.sh", shell=True)
                        except Exception as e:
                            logging.error("Exception on merge_notification. {}".format(str(e)))

    return ""

@blueprint.route("/deploy", methods=['POST'])
def deploy_call():
    if request.form['username'] == USER_ADMIN and request.form['password'] == PASSWORD_ADMIN:
        try:
            result = subprocess.call(ROOT+"/deploy.sh", shell=True)
        except Exception as e:
            logging.error("Exception on deploy_call. {}".format(str(e)))
            return "error. {} \n".format(str(e))
    else:
        return "username or password not valid"

    return "ok\n"

def send_confirm_email(msg, tpl):
    try:
        html = codecs.open(ROOT+"/main/email/{}".format(tpl), 'r').read()
        html = html.replace("$1", msg)
        html = html.replace("$2", url_for('main.contact_page', _external=True))
        send_email_helper(subject='Contact message', message_body=html, to=EMAIL)
    except Exception as e:
        raise Exception("Exception on send_confirm_email. {}".format(str(e)))


def reverse_filter(arr):
    status = 0
    if current_user.status != None:
        status = current_user.status

    arr.reverse()
    if len(arr) >= 3:
        if status == 0:
            return [ arr[i] for i in (0, 1, 2) if i <= 2]
        elif status == 1:
            return arr
        elif status == -1:
            return ['Blocked']
    else:
        if status == -1:
            return ['Blocked']
        else:
            return arr

# --------------------------------------------
# ----------------- Guide ------------------
# --------------------------------------------

@blueprint.route("/set-guide-status", methods=['POST'])
def set_guide_status():
    show = request.form['show']
    resource = request.form['resource']
    print(show)
    print(resource)
    unique_id = str(uuid.uuid1())
    try:
        uru = UserResourceUsage(id=unique_id,resource_name=resource, term="", result="", user_id=current_user.id, search_date=calendar.timegm(time.gmtime()), showTour=False)
        db.session.add(uru)
        db.session.commit()
    except Exception as e:
        print(e)

    return "ok"

@blueprint.route("/get-guide-status", methods=['POST'])
def get_guide_status():
    user = current_user
    resource = request.form['resource']

    for res in user.urusages:
        if resource == res.resource_name and current_user.id == res.user_id:
            return jsonify({
                "status": res.showTour,
            })

    return jsonify({
        "status": True,
    })

@blueprint.route("/retrieve-emails", methods=['GET'])
@login_required
def retrieve_emails():
    # if request.form['username'] == USER_ADMIN and request.form['password'] == PASSWORD_ADMIN:
    if current_user.is_admin == True:
        try:
            emails = ""
            users = User.query.order_by(User.email).all()
            for user in users:
                if user.email == 'admin_seana':
                    continue
                emails += user.email + ", "
        except Exception as e:
            logging.error("Exception on deploy_call. {}".format(str(e)))
            return "error. {} \n".format(str(e))
    else:
        return "You must have permission to access this content "
    return render_template(templates_path + "emails_list.html", emails=emails)
