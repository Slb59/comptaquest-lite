from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CQUser(auth_models.AbstractUser):

    class UserTypes(models.TextChoices):
        ACCOUTANT = "accountant", "Accountant"
        MEMBER = "member", "Member"
        SUPERMEMBER = "supermember", "Supermember"

    first_name = None
    last_name = None
    username = None
    email = models.EmailField(_("email address"), unique=True, max_length=50)
    trigram = models.CharField(max_length=5, blank=False)
    usertype = models.CharField(
        max_length=30, choices=UserTypes.choices, default=UserTypes.MEMBER, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["trigram"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.trigram}"

    class Meta:
        verbose_name_plural = "users"
        verbose_name = "user"
        ordering = ["-trigram"]
        indexes = [
            models.Index(fields=["-trigram"]),
        ]


class BaseUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="_profile"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(blank=True, upload_to="profile_images")

    class Meta:
        abstract = True

    def __str__(self):
        return f"Profile of {self.user.trigram}"


class MemberProfile(BaseUserProfile):
    """specific data to member"""

    ...


class MemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(usertype=CQUser.UserTypes.MEMBER)


class Member(CQUser):

    class Meta:
        proxy = True

    member = MemberManager()

    @property
    def profile(self):
        try:
            return self._profile
        except MemberProfile.DoesNotExist:
            return MemberProfile.objects.create(
                user=self,
            )


@receiver(post_save, sender=Member)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.usertype == "MEMBER":
        MemberProfile.objects.create(user=instance)
