from django.core.management.base import BaseCommand

from secretbox.users.models import Member


class Command(BaseCommand):
    help = "Create user test for Playwright"

    def handle(self, *args, **options):
        users = Member.objects.all()
        for user in users:
            user.set_password("motdepasse2")
            user.save()
