from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from secretbox.tools.date_tools import get_now_date
from secretbox.tools.models_tools import bounded_integer_field

from .descriptions import SAMI_DESCRIPTIONS


class Sami(models.Model):
    date = models.DateField(default=get_now_date)
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    bedtime = bounded_integer_field(0, 3, "Saisir une valeur entre 0 et 3")

    wakeup = bounded_integer_field(0, 3, "Saisir une valeur entre 0 et 3")

    nonstop = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    energy = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    naptime = bounded_integer_field(0, 4, "Saisir une valeur entre 0 et 4")

    phone = bounded_integer_field(0, 2, "Saisir une valeur entre 0 et 2")

    reading = bounded_integer_field(0, 3, "Saisir une valeur entre 0 et 3")

    fruits = bounded_integer_field(0, 3, "Saisir une valeur entre 0 et 3")

    vegetables = bounded_integer_field(0, 2, "Saisir une valeur entre 0 et 2")

    meals = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    desserts = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    sugardrinks = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    nosugardrinks = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    homework = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    garden = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    outsidetime = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    endurancesport = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    yogasport = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    videogames = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    papergames = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    administrative = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    computer = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    youtube = bounded_integer_field(0, 5, "Saisir une valeur entre 0 et 5")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_diaries",
        db_index=True,
    )

    @property
    def metrics(self):
        from .samimetrics_model import SamiMetrics

        return SamiMetrics(self)

    def __str__(self):
        return f"Sami data {self.date}"

    def get_description(self, field: str) -> str:
        return SAMI_DESCRIPTIONS.get(field, "")

    class Meta(TypedModelMeta):
        verbose_name = _("Sami")
        verbose_name_plural = _("Samis")
        ordering = ["date"]
