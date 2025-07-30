from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from secretbox.tools.models import get_now_date


class Sami(models.Model):
    date = models.DateField(default=get_now_date)
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    bedtime = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=_("Saisir une valeur entre 0 et 3"),
        default=0,
    )
    wakeup = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=_("Saisir une valeur entre 0 et 3"),
        default=0,
    )
    nonstop = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )
    energy = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )
    naptime = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        help_text=_("Saisir une valeur entre 0 et 4"),
        default=0,
    )
    phone = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_("Saisir une valeur entre 0 et 2"),
        default=0,
    )
    reading = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=_("Saisir une valeur entre 0 et 3"),
        default=0,
    )

    fruits = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=_("Saisir une valeur entre 0 et 3"),
        default=0,
    )

    vegetables = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_("Saisir une valeur entre 0 et 2"),
        default=0,
    )

    meals = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    desserts = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    sugardrinks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    nosugardrinks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    homework = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    garden = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    Outsidetime = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    endurancesport = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    yogasport = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    videogames = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    papergames = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    administrative = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    computer = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
    )

    youtube = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Saisir une valeur entre 0 et 5"),
        default=0,
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
        return _(
            "Heure de réveil (0: < 5h30, 3: 5h30-7h30, 2: 7h30-8h00, 1: 8h00-9h00, 0: >9h00)"
        )

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
        return _(
            "Lecture (3: > 30mn,2: <30mn concentrée, 1: <30mn non concentrée, 0: si absence)"
        )

    @property
    def total_sleep(self):
        return (
            self.bedtime
            + self.wakeup
            + self.nonstop
            + self.energy
            + self.naptime
            + self.phone
            + self.reading
        )

    @property
    def total_sleep_description(self):
        return _("Total Sommeil : maxi 25")

    @property
    def fruits_description(self):
        return _("1 par fruit, maxi 3")

    @property
    def vegetables_description(self):
        return _("1 par légume, maxi 2")

    @property
    def meals_description(self):
        return _(
            "selon la qualité du plat, +1 s'il y a au moins 3 ingrédients différents, +1 s'il y a des légumes, -3 s'il y a des pâtes ou du pain"
        )

    @property
    def desserts_description(self):
        return _(
            "0 si le dessert est trop calorique (chocolat ou gâteau), +2 ou +3 s'il est fait maison, +1 s'il est léger (yaourt)"
        )

    @property
    def sugardrinks_description(self):
        return _(
            "0 si il est trop calorique (coca), -2 si c'est du sirop, -2 si sucre ajouté (dans le thé ou le café par exemple)"
        )

    @property
    def nosugardrinks_description(self):
        return _("+1 par verre")

    @property
    def total_food(self):
        return (
            self.fruits
            + self.vegetables
            + self.meals
            + self.desserts
            + self.sugardrinks
            + self.nosugardrinks
        )

    @property
    def total_food_description(self):
        return _("Total Alimentation : maxi 25")

    @property
    def homework_description(self):
        return _("5 si > 2h, 4 si entre 1h et 2h, 3 si 30mn-1h, 2 si < 30mn")

    @property
    def garden_description(self):
        return _(
            "5 si > 2h,  4 si entre 1h et 2h, 3 si 30mn-1h, 2 si < 30mn,   0 sinon"
        )

    @property
    def Outsidetime_description(self):
        return _("5 si > 3h ,4 si entre 2 et 3h, 3 entre 1 et 2h, 0 sinon")

    @property
    def endurancesport_description(self):
        return _(
            "Natation-course-velo: 5 si > 1h ,4 si entre 30mn et 1h ,2 si <30mn, 0 si rien"
        )

    @property
    def yogasport_description(self):
        return _("Yoga-musculation,5 si >1h ,4 si >30mn ,2 si < 30mn ,0 sinon")

    @property
    def total_move(self):
        return (
            self.homework
            + self.garden
            + self.Outsidetime
            + self.endurancesport
            + self.yogasport
        )

    @property
    def total_move_description(self):
        return _("Total Mouvement : maxi 25")

    @property
    def videogames_description(self):
        return _("5 >1h30, 3: entre 1h30 et 2h, 2 si 0, 0 sinon")

    @property
    def papergames_description(self):
        return _("5 si entre 2 et 3h ,4 si entre 1 et 2h ou > 3h ,3 si < 1h, 0 si > 3h")

    @property
    def administrative_description(self):
        return _("5 si entre 2 et 3h ,4 si entre 1 et 2h ou > 3h ,3 si < 1h, 0 si > 3h")

    @property
    def computer_description(self):
        return _("5 si entre 4 et 5h ,3 si > 5 ,4 si entre 2 et 4h ,3 si 1 à 2h")

    @property
    def youtube_description(self):
        return _("5 si < 1h ,3 si entre 1h et 2h ,0 si > 2h")

    @property
    def total_idea(self):
        return (
            self.computer
            + self.youtube
            + self.administrative
            + self.papergames
            + self.videogames
        )

    @property
    def total_idea_description(self):
        return _("Total idées : maxi 25")

    @property
    def total_sami(self):
        return self.total_sleep + self.total_food + self.total_move + self.total_idea

    @property
    def total_sami_description(self):
        return _("Total Sami : maxi 100")

    def __str__(self):
        return f"Sami data {self.date}"

    class Meta(TypedModelMeta):
        verbose_name = _("Sami")
        verbose_name_plural = _("Samis")
        ordering = ["date"]
