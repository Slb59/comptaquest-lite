from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class Sami(models.Model):
    date = models.DateField(default=datetime.now())
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    bedtime = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], help_text=_("Saisir une valeur entre 0 et 3")
    )
    wakeup = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], help_text=_("Saisir une valeur entre 0 et 3")
    )
    nonstop = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], help_text=_("Saisir une valeur entre 0 et 5")
    )
    energy = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], help_text=_("Saisir une valeur entre 0 et 5")
    )
    naptime = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)], help_text=_("Saisir une valeur entre 0 et 4")
    )
    phone = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)], help_text=_("Saisir une valeur entre 0 et 2")
    )
    reading = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], help_text=_("Saisir une valeur entre 0 et 3")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_diaries",
        db_index=True,
    )

    @property
    def bedtime_description(self):
        return _("Heure du coucher (0: > 23h, 3: 22h-23h, 2: 21h-22h, 1: <21h)")

    @property
    def wakeup_description(self):
        return _("Heure de réveil (0: < 5h30, 3: 5h30-7h30, 2: 7h30-8h00, 1: 8h00-9h00, 0: >9h00)")

    @property
    def nonstop_description(self):
        return _(
            "Temps non stop (0: < 4h00, 1: 4h00-5h00,2: 5h00-6h00, 3: 6h00-7h00, 5: 7h00-8h00, 2: 8h00-10h00, 0: >10h00)"
        )

    @property
    def energy_description(self):
        return _(
            "Forme (5: je fais plein de chose, je ne suis pas fatiguée, 1:je ne pleure pas mais je me lutte contre la fatigue toute la journée, 0:dépression)"
        )

    @property
    def naptime_description(self):
        return _("Sieste (4: 15-20 mn, 2: < 15mn, 2: 20mn-1h, 0: > 1h)")

    @property
    def phone_description(self):
        return _("Telephone (2: absence, 1: Présence, 0: présence et usage)")

    @property
    def reading_description(self):
        return _("Lecture (3: > 30mn,2: <30mn concentrée, 1: <30mn non concentrée, 0: si absence)")

    @property
    def total_sleep(self):
        return self.bedtime + self.wakeup + self.nonstop + self.energy + self.naptime + self.phone + self.reading

    @property
    def total_sleep_description(self):
        return _("Total Sommeil : maxi 25")

    def __str__(self):
        return f"Sami data {self.date}"

    class Meta(TypedModelMeta):
        verbose_name = _("Sami")
        verbose_name_plural = _("Samis")
        ordering = ["date"]
