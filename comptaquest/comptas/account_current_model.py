from django.db import models

from .account_abstract_model import AbstractAccount


class CurrentAccount(AbstractAccount):
    account_type = models.CharField(
        max_length=15,
        default="Current",
        editable=False,  # Fixed account type
    )
