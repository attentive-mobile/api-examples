#! /usr/bin/env python3.7

"""
This is an example of a basic flask app that performs the Authorization Code OAuth2 flow
to authenticate against Attentive

More details can be found at https://docs.attentivemobile.com/pages/authentication/
"""
import os
from datetime import datetime
import random
import string
import json
import hmac
import hashlib
import base64

import requests
from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv, find_dotenv

from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

ATTENTIVE_API_URL = "https://api.attentivemobile.com/v1/"
ACCESS_TOKEN_ENDPOINT = (
    "https://api.attentivemobile.com/v1/authorization-codes/tokens"
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Applications(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String())
    name = db.Column(db.String())
    state = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<application <id {self.id}>"


db.init_app(app)
db.create_all()


@app.route("/install")
def redirect_to_install_page():
    # Generates a random string containing numbers and letters
    state = "".join(random.choice(string.ascii_lowercase) for i in range(10))

    # List of scopes that your app needs
    scopes = ["ecommerce:write", "events:write", "subscriptions:write"]

    application = Applications(state=state)
    db.session.add(application)
    db.session.commit()

    # this is the Attentive url for authorizing your application
    redirect_url = (
        f"https://ui.attentivemobile.com/integrations/oauth-install?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f'&scope={"+".join(scopes)}'
        f"&state={state}"
    )

    # Your application requests authorization
    return redirect(redirect_url, code=302)


@app.route("/callback")
def redirect_from_install_page():
    authorization_code = request.args.get("authorizationCode")
    state = request.args.get("state")

    application: Applications = Applications.query.filter_by(state=state).first()
    if not application:
        return "no application"

    # your application makes a request to exchange an authorization code for an access_token
    response = requests.post(
        ACCESS_TOKEN_ENDPOINT,
        json={
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    access_token = response.json().get("access_token")
    if not access_token:
        return "no token"

    # make a request to /me endpoint to access Attentive API
    me_response = requests.get(
        ATTENTIVE_API_URL + "me",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    company_name = me_response.json().get("companyName")

    # store access token and information about the installing company if necessary
    application.token = access_token
    application.name = company_name
    db.session.add(application)
    db.session.commit()
    return jsonify({"response": "Company Successfully Installed"})


"""
This is an example of a webhook receive endpoint.  

In order to run locally, we recommend using a tunneling tool such as ngrok (https://ngrok.com/) 
"""


@app.route("/webhooks", methods=['POST'])
def webhook_received():
    webhook_secret = os.getenv('WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('x-attentive-hmac-sha256')

        # Retrieve the event by verifying the signature using the raw body
        # and secret if webhook signing is configured.
        try:
            digest = hmac.new(bytes(webhook_secret, 'utf-8'),
                              msg=request.data,
                              digestmod=hashlib.sha256).hexdigest()
            valid = hmac.compare_digest(digest, signature)
            if not valid:
                print(f'🔔 Webhook received with invalid signature!')
                return jsonify({'status': 'invalid signature'}), 403
        except Exception as e:
            return e

    event_type = request_data["type"]
    print(f'🔔 Webhook of type {event_type} received!')
    return jsonify({'status': 'success'}), 200
