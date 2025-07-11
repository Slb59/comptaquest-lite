from django.contrib.sessions.backends.db import SessionStore
from django.test import Client
from tests.factories.member import MemberFactory

def create_logged_in_session():
    user = MemberFactory(email="testuser@test.com", password="testpass")

    client = Client()
    client.login(username="testuser", password="testpass")

    sessionid = client.cookies["sessionid"].value
    return sessionid
