from secretbox.users.models import Member
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user test for Playwright"

    def handle(self, *args, **options):
        users = Member.objects.all()
        for user in users:
            user.set_password("motdepasse2")
            user.save()