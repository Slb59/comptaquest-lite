from django.test import Client

from tests.factories.member import MemberFactory


def create_logged_in_session():
    user = MemberFactory(email="test.user@test.com", password="motdepasse2")  # nosec B106
    user.save()

    client = Client()
    client.login(email="test.user@test.com", password="motdepasse2")  # nosec B106

    sessionid = client.cookies["sessionid"].value
    return sessionid
