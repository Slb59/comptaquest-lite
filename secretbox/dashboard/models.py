# dashboard.models.py
from datetime import date, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from threadlocals.threadlocals import get_current_request

from secretbox.users.models import CQUser as User


class Todo(models.Model):
    """
    Model representing a task to be accomplished in the system.

    This model allows you to manage tasks with their status, priority, category and assignment.
    It also includes the ability to schedule recurring tasks and associate them with a specific user.

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
        category (CharField): Catégorie de la tâche :
            - organisation: Organisation
            - compta: Compta
            - achat: Achats
            - sport: Sport
            - sante: Santé
            - contact: Contact
            - informatique: Informatique
            - menage: Menage
            - jardin: Jardin
            - doudou: Doudou
            - bricoles: Bricoles
            - couture: Couture
            - loisirs: Loisirs
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
        periodic (CharField): Fréquence de répétition :
            - none: Une seule fois
            - everyday: Tous les jours
            - every2days: Tous les 2 jours
            - every3days: Tous les 3 jours
            - everyweek: Toutes les semaines
            - etc.
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
    PRIORITY_CHOICES = [
        ("6-verylow", "Très faible"),
        ("5-low", "Faible"),
        ("4-normal", "Normale"),
        ("3-medium", "Moyenne"),
        ("2-high", "Élevée"),
        ("1-highest", "Trés élevée"),
    ]
    CATEGORY_CHOICES = [
        ("01-organisation", "Organisation"),
        ("02-compta", "Compta"),
        ("03-achat", "Achats"),
        ("04-sport", "Sport"),
        ("05-sante", "Santé"),
        ("06-contact", "Contact"),
        ("07-informatique", "Informatique"),
        ("08-menage", "Menage"),
        ("09-jardin", "Jardin"),
        ("10-doudou", "Doudou"),
        ("11-bricoles", "Bricoles"),
        ("12-couture", "Couture"),
        ("13-loisirs", "Loisirs"),
    ]
    WHO_CHOICES = [
        ("SLB", "Sylvie"),
        ("JCB", "Jean-Christophe"),
        ("LAU", "Laurine"),
        ("THO", "Thomas"),
        ("ODI", "Odile"),
        ("MAM", "Maman"),
        ("PAP", "Papa"),
    ]
    PLACE_CHOICES = [
        ("cantin", "Cantin"),
        ("chm", "CHM"),
        ("genese", "Genèse"),
        ("partout", "Partout"),
    ]
    PERIODIC_CHOICES = [
        ("01-none", "une seule fois"),
        ("02-everyday", "Tous les jours"),
        ("03-every2days", "Tous les 2 jours"),
        ("04-every3days", "Tous les 3 jours"),
        ("05-every4days", "Tous les 4 jours"),
        ("06-every5days", "Tous les 5 jours"),
        ("07-everyweek", "Toutes les semaines"),
        ("08-every10days", "Tous les 10 jours"),
        ("09-every2weeks", "Toutes les 2 semaines"),
        ("10-everymonth", "Tous les mois"),
        ("11-every6weeks", "Toutes les 6 semaines"),
        ("12-every2months", "Tous les 2 mois"),
        ("13-every3months", "Tous les 3 mois"),
        ("14-every4months", "Tous les 4 mois"),
        ("15-every6months", "Tous les 6 mois"),
        ("16-everyyear", "Tous les ans"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="todo")
    duration = models.IntegerField(default=30, validators=[MinValueValidator(10), MaxValueValidator(800)])
    description = models.TextField()
    appointment = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="01-organisation")
    who = models.CharField(max_length=20, choices=WHO_CHOICES, default="SLB")
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default="partout")
    periodic = models.CharField(max_length=20, choices=PERIODIC_CHOICES, default="partout")
    report_date = models.DateField(blank=True, null=True)
    planned_date = models.DateField(default=(date.today() + timedelta(days=1)))
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="4-normal")
    done_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

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

        if self.state != "done" and new_date > self.planned_date:
            self.planned_date = new_date
            self.report_date = None
            self.done_date = date_to_validate
            self.state = "todo"
            self.save()
            return True
        else:
            return False

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
        self.state = "done"
        self.done_date = date_of_done
        self.save()
 
    def get_appointment_display(self):
        """
        Returns the formatted appointment or an empty string if None.
        Returns:
            str: The formatted appointment or an empty string.
        """
        return self.appointment.strftime("%d/%m/%Y %H:%M") if self.appointment else ""