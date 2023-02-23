# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
from flask import request, jsonify
from flask import redirect, url_for
from flask import Blueprint, render_template
import json
import os
from config.config import STRIP_API_KEY
from config.config import STRIPE_WEBHOOK_SECRET
from config.config import STRIPE_PUBLISHABLE_KEY
from db.token_offers import TokenOffers
import stripe
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from db.user import User
from db.db import db
from db.token_offers import TokenOffers

stripe.api_key = STRIP_API_KEY


blueprint = Blueprint('payment', __name__,
                      template_folder='../',
                      static_url_path='/static',
                      static_folder='../static')

@blueprint.route('/setup', methods=['PUT'])
def get_publishable_key():
    name = json.loads(request.data)
    print(name)
    offer = TokenOffers.query.filter_by( name=name ).first()
    price_id = offer.price_id
    return jsonify({
        'publishableKey': STRIPE_PUBLISHABLE_KEY,
        'tagSearchPriceId': price_id
    })

@blueprint.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)

    try:
        # See https://stripe.com/docs/api/checkout/sessions/create
        # for additional parameters to pass.
        # {CHECKOUT_SESSION_ID} is a string literal; do not change it!
        # the actual Session ID is returned in the query parameter when your customer
        # is redirected to the success page.
        checkout_session = stripe.checkout.Session.create(
            success_url=request.url_root+"checkout-session?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.url_root+"dashboard",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price": data['priceId'],
                    # For metered billing, do not pass quantity
                    "quantity": 1
                }
            ],
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400

@blueprint.route('/checkout-session', methods=['GET'])
def checkout_session():
    id = request.args.get('session_id')
    print(id)
    checkout_session = stripe.checkout.Session.retrieve(id)
    if checkout_session != None:
        user = User.query.filter_by(id=current_user.id).first()
        user.stripe_session = checkout_session['id']
        cents = checkout_session['amount_total']
        user.token_amount += cents
        db.session.commit()

    return redirect(url_for("main.index"))

@blueprint.route('/customer-portal', methods=['GET'])
def customer_portal():
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    user = User.query.filter_by(id=current_user.id).first()
    checkout_session_id = user.stripe_session
    print("""
    ####################################################
    
    
    """)
    print(user.name)
    print(user.stripe_session)
    print(user.email)
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = request.url_root

    session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url)
    print(return_url)
    return jsonify({'url': session.url})

@blueprint.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.data)
    user = User.query.filter_by(id=current_user.id).first()
    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
        # Payment is successful and the subscription is created.
        # You should provision the subscription.
        
        print(data)
    elif event_type == 'invoice.paid':
        # Continue to provision the subscription as payments continue to be made.
        # Store the status in your database and check when a user accesses your service.
        # This approach helps you avoid hitting rate limits.
        print(data)
    elif event_type == 'invoice.payment_failed':
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        print(data)
    else:
        print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})