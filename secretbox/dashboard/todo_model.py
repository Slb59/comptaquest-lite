# secretbox.dashboard.models.py
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .choices import CATEGORY_CHOICES, PERIODIC_CHOICES, PLACE_CHOICES, PRIORITY_CHOICES
from .colorparameter_model import ColorParameter

User = get_user_model()

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Entrez une couleur au format hexadécimal valide (ex: #1A2B3C).",
)


class Todo(models.Model):
    """
    Model representing a task to be accomplished in the system.

    This model allows you to manage tasks
    with their status, priority, category and assignment.
    It also includes the ability to schedule recurring tasks
    and associate them with a specific user.

    Attributs:
        state (CharField): État de la tâche avec les choix suivants :
            - todo: À faire
            - in_progress: En cours
            - done: Terminé
            - report: Reporté
        priority (CharField): Niveau de priorité de la tâche :
            - 6-verylow: Très faible
            - 5-low: Faible
            - 4-normal: Normale
            - 3-medium: Moyenne
            - 2-high: Élevée
            - 1-highest: Très élevée
        category (CharField): Catégorie de la tâche
        who (CharField): Personne responsable avec les choix suivants :
            - SLB: Sylvie
            - JCB: Jean-Christophe
            - LAU: Laurine
            - THO: Thomas
            - ODI: Odile
            - MAM: Maman
            - PAP: Papa
        place (CharField): Lieu où la tâche doit être effectuée :
            - cantin: Cantin
            - chm: CHM
            - genese: Genèse
            - partout: Partout
        periodic (CharField): Fréquence de répétition
        duration (DurationField): Durée estimée pour accomplir la tâche
        description (TextField): Description détaillée de la tâche
        appointment (DateTimeField): Date et heure prévue pour la tâche
        date (DateField): Date de création de la tâche
        done (DateField): Date de réalisation de la tâche
        note (TextField): Notes supplémentaires (optionnel)

    Méthodes:
        __str__(): Returns the task description as a string representation.
    """

    STATE_CHOICES = [
        ("todo", "À faire"),
        ("in_progress", "En cours"),
        ("done", "Terminé"),
        ("report", "Reporté"),
        ("cancel", "Annulé"),
    ]

    APPOINTEMENT_CHOICES = [
        ("rdv", "Rendez-vous"),
        ("birthday", "Anniversaire"),
        ("festival", "Fête"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_todos"
    )
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="todo")
    duration = models.IntegerField(
        default=30, validators=[MinValueValidator(10), MaxValueValidator(800)]
    )
    description = models.TextField()
    appointment = models.CharField(
        max_length=20, choices=APPOINTEMENT_CHOICES, blank=True, null=True
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="01-organisation"
    )
    who = models.ManyToManyField(User, related_name="assigned_todos", blank=True)
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default="partout")
    periodic = models.CharField(
        max_length=20, choices=PERIODIC_CHOICES, default="partout"
    )
    report_date = models.DateField(blank=True, null=True)
    planned_date = models.DateField(default=(date.today() + timedelta(days=1)))
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="4-normal"
    )
    done_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

    def check_if_state_is_cancel_or_done(self):
        if self.state == "done":
            return False, _("Cette tâche est déjà terminée")
        if self.state == "cancel":
            return False, _("Cette tâche est déjà annulée")
        return True, ""

    def validate_element(self, new_date, date_to_validate=date.today()):
        """
        Validates and updates a Todo element's planned_date if the new date is in the future.

        This method checks if the provided date is later than the current date and
        updates the element's date accordingly. The changes are automatically saved
        to the database if the update is successful.

        Args:
            new_date (date): The new date to validate and potentially set

        Returns:
            bool: True if the date was updated, False if the new date is not later than current date
        """
        if self.state in ("done", "cancel"):
            return False, _("Cette tâche est déjà terminée ou annulée.")

        if new_date <= self.planned_date:
            return False, _(
                "La date doit être postérieure à la date planifiée actuelle."
            )

        self.planned_date = new_date
        self.report_date = None
        self.done_date = date_to_validate
        self.state = "todo"
        self.save()
        return True, ""

    def next_date(self):
        """
        Calculate the next date based on the periodicity choice.

        Returns:
            date: The next date calculated according to the periodicity
        """
        PERIODIC_DAYS_MAPPING = {
            "02-everyday": 1,
            "03-every2days": 2,
            "04-every3days": 3,
            "05-every4days": 4,
            "06-every5days": 5,
            "07-everyweek": 7,
            "08-every10days": 10,
            "09-every2weeks": 14,
            "10-everymonth": 30,
            "11-every6weeks": 42,
            "12-every2months": 60,
            "13-every3months": 90,
            "14-every4months": 120,
            "15-every6months": 180,
            "16-everyyear": 365,
        }

        days_to_add = PERIODIC_DAYS_MAPPING[self.periodic]
        return self.planned_date + timedelta(days=days_to_add)

    def report_element(self, date_of_report=date.today()):
        """
        Reports the element to the user.

        This method sets the element's state to "report" and updates the date to the next date.
        The changes are automatically saved to the database if the update is successful.
        """
        if self.state != "done":
            self.planned_date = date_of_report + timedelta(days=1)
            self.state = "report"
            if self.report_date is None:
                self.report_date = date_of_report
            self.save()

    def new_day(self, new_planned_date=date.today()):
        """
        Updates the element's current date to now.
        Updates all planned dates to now.
        set the state to "report" if the element is not done.

        This method updates the element's current date to the next day and saves the changes.

        """
        if self.state != "done" and self.planned_date < new_planned_date:
            self.planned_date = new_planned_date
            self.state = "report"
            if self.report_date is None:
                self.report_date = new_planned_date
            self.save()

    def set_done(self, date_of_done=date.today()):
        """
        Sets the element's state to "done" and updates the date done_date.
        """
        if self.state != "cancel":
            self.state = "done"
            self.done_date = date_of_done
            self.save()
            return True
        return False

    def get_planned_date_display(self):
        """
        Returns the formatted planned_date or an empty string if None.
        Returns:
            str: The formatted planned_date or an empty string.
        """
        return self.planned_date.strftime("%d/%m/%Y") if self.planned_date else ""

    def get_done_date_display(self):
        """
        Returns the formatted done_date or an empty string if None.
        Returns:
            str: The formatted done_date or an empty string.
        """
        return self.done_date.strftime("%d/%m/%Y") if self.done_date else ""

    def get_color(self) -> str:
        filters = [
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category=self.category,
                place=self.place,
            ),
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category=self.category,
                place="*-Every",
            ),
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category="*-Every",
                place="*-Every",
            ),
            Q(
                priority=self.priority,
                periodic="*-Every",
                category="*-Every",
                place="*-Every",
            ),
        ]

        for f in filters:
            color_param = ColorParameter.objects.filter(f).first()
            if color_param:
                return color_param.color

        return "#f3faf0"  # Couleur par défaut

    def can_view(self, user):
        return (
            user.is_superuser
            or self.user == user
            or self.who.filter(pk=user.pk).exists()
        )

    def can_edit(self, user):
        return user.is_superuser or self.user == user

    def can_edit_limited(self, user):
        return (
            self.who.filter(pk=user.pk).exists()
            and self.user != user
            and not user.is_superuser
        )

    def can_delete(self, user):
        return user.is_superuser or self.user == user

    def can_edit_any(self, user):
        return self.can_edit(user) or self.can_edit_limited(user)
