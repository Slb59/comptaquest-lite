from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Ledger(models.Model):
    class LedgerState(models.TextChoices):
        CLOSED = "Closed", "closed"
        OPEN = "Open", "open"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_ledgers",
        db_index=True,
    )
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=LedgerState.choices, default=LedgerState.OPEN)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date cannot be later than end_date.")
