from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class DiaryEntry(models.Model):
    """
    A model representing a single diary entry written by a user.

    Attributes:
        date (DateField): The date this diary entry was written
        content (TextField): The actual text content of the diary entry
        created_at (DateTimeField): Timestamp when the entry was created
        updated_at (DateTimeField): Timestamp when the entry was last modified
        user (ForeignKey): The user who wrote this diary entry

    Relationships:
        - Each diary entry belongs to exactly one user
        - Users can have multiple diary entries
    """

    date = models.DateField(default=datetime.now(), help_text=_("Date when this diary entry was written"))
    content = models.TextField(blank=True, help_text=_("The main content of the diary entry"))
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, help_text=_("Timestamp when this entry was created")
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, help_text=_("Timestamp when this entry was last modified")
    )
    # Foreign key to the user model
    # Delete the diary entry if the user is deleted
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_diaries",
        db_index=True,
        help_text=_("User who created this diary entry"),
    )

    def __str__(self):
        """
        Returns a human-readable string representation of the diary entry.

        Returns:
            str: A string in the format 'Entry from YYYY-MM-DD'
        """
        return f"Entry from {self.date}"

    class Meta(TypedModelMeta):
        """
        Metadata options for the DiaryEntry model.

        Attributes:
            verbose_name: Singular human-readable name ('Pensée')
            verbose_name_plural: Plural human-readable name ('Pensées')
            ordering: Default ordering by date
        """

        verbose_name = _("Pensée")
        verbose_name_plural = _("Pensées")
        ordering = ["date"]
