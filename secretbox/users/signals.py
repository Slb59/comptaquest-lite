from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MemberProfile

Member = get_user_model()


@receiver(post_save, sender=Member)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.usertype == "MEMBER":
        MemberProfile.objects.create(user=instance)
