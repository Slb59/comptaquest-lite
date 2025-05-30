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
    usertype = models.CharField(max_length=30, choices=UserTypes.choices, default=UserTypes.MEMBER, blank=True)

    last_password_change = models.DateTimeField(
        _("Dernier changement de mot de passe"),
        null=True,
        blank=True
    )
    last_email_change = models.DateTimeField(
        _("Dernier changement d'email"),
        null=True,
        blank=True
    )
    last_trigram_change = models.DateTimeField(
        _("Dernier changement de trigram"),
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["trigram"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.trigram}"

    def can_modify_apps(self):
        """Permet de savoir si l'utilisateur a les droits pour modifier les apps"""
        return self.usertype == self.UserTypes.SUPERMEMBER or self.is_staff

    def request_app_modification(self, requested_apps):
        """Envoie un mail à l'administrateur pour demander la modification des apps"""
        from django.core.mail import send_mail
        from django.conf import settings

        subject = f"Demande de modification d'applications pour {self.trigram}"
        message = f"""
        L'utilisateur {self.trigram} ({self.email}) a demandé une modification de ses applications autorisées.
        Applications demandées : {', '.join(requested_apps)}

        Veuillez traiter cette demande via l'interface d'administration.
        """

        send_mail(
            subject,
            message,
            self.email,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    class Meta:
        verbose_name_plural = "users"
        verbose_name = "user"
        ordering = ["-trigram"]
        indexes = [
            models.Index(fields=["-trigram"]),
        ]


class BaseUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="_profile")
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



