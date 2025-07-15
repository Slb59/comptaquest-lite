from django.test import Client

from tests.factories.member import MemberFactory


def create_logged_in_session():
    user = MemberFactory(email="testuser@test.com", password="testpass")
    user.save()

    client = Client()
    client.login(username="testuser", password="testpass")

    sessionid = client.cookies["sessionid"].value
    return sessionid
