from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'List all users'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        self.stdout.write("Liste des utilisateurs")
        for user in users:
            self.stdout.write(f"Username: {user.trigram}, Email: {user.email}")
