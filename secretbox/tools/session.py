from django.test import Client

from tests.factories.member import MemberFactory


def create_logged_in_session():
    user = MemberFactory(email="test.user@test.com", password="motdepasse2")
    user.save()

    client = Client()
    client.login(email="test.user@test.com", password="motdepasse2")

    sessionid = client.cookies["sessionid"].value
    return sessionid
