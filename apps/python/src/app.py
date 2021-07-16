#! /usr/bin/env python3.7

"""
This is an example of a basic flask app that performs the Authorization Code OAuth2 flow
to authenticate against Attentive
"""
import os
from datetime import datetime
import random
import string

import requests
from flask import Flask, redirect, request
from dotenv import load_dotenv, find_dotenv

from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# TODO: move to prod when we eventually make this public
ATTENTIVE_API_URL = "https://api-devel.attentivemobile.com/v1/"
ACCESS_TOKEN_ENDPOINT = (
    f"https://api-devel.attentivemobile.com/v1/authorization-codes/tokens"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////code/data/demo.sqlite"
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

    # TODO: move to prod and delete internal note when we eventually make this public
    # Note: to internal devs, feel free to use localhost:4000 when testing in dev
    redirect_url = (
        f"https://ui-devel.attentivemobile.com/integrations/oauth-install?client_id={CLIENT_ID}"
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
            "grantType": "authorization_code",
            "code": authorization_code,
            "redirectUri": REDIRECT_URI,
            "clientId": CLIENT_ID,
            "clientSecret": CLIENT_SECRET,
        },
    )

    access_token = response.json().get("token")
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
    return "Company Successfully Installed"
