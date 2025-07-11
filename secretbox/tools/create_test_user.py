from django.core.management.base import BaseCommand
from secretbox.users.models import Member
from tests.factories.member import MemberFactory

class Command(BaseCommand):
    help = 'Create user test for Playwright'

    def handle(self, *args, **options):
        email = 'test.user@test.com'
        password = 'motdepasse'
        if not Member.objects.filter(email=email).exists():
            user = MemberFactory(email=email, password=password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Utilisateur {username} créé"))
        else:
            self.stdout.write(self.style.WARNING(f"L'utilisateur {username} existe déjà."))
