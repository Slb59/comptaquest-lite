from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta
from django.conf import settings
from datetime import datetime


class DiaryEntry(models.Model):
    date = models.DateField(default=datetime.now())
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_diaries",
        db_index=True,
    )

    def __str__(self):
        return f"Entry from {self.date}"

    class Meta(TypedModelMeta):
        verbose_name = _("Pensée")
        verbose_name_plural = _("Pensées")
        ordering = ["date"]

