"""


This is a test suite for our webhooks and /pay endpoints.
It uses the data mocked in test_data.py to create sample requests and responses.
"""

import json
# import os
from unittest import TestCase
from dotenv import load_dotenv, find_dotenv

import sys

sys.path.append('../')
import pytest
from urllib.parse import parse_qs

from app import app as flask_app, db, Applications

@pytest.fixture
def client():
    app = flask_app.test_client()
    app.testing = True
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def application():
    application = Applications(state='test_state')
    db.session.add(application)
    db.session.commit()



def test_redirect_to_install_page(client):
    response = client.get('install')

    assert response.status_code == 302


def test_redirect_to_install_page_application_created(client):
    response = client.get('install')
    redirect_url = response.headers.get('Location')
    params = parse_qs(redirect_url)
    state = params['state'][0]

    assert Applications.query.filter_by(state=state).first() is not None
