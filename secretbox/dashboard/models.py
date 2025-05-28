# models.py
from django.db import models
from secretbox.users.models import CQUser as User

class Todo(models.Model):
    STATE_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('report', 'Reporté'),
    ]
    PRIORITY_CHOICES = [
        ('6-verylow', 'Très faible'),
        ('5-low', 'Faible'),
        ('4-normal', 'Normale'),        
        ('3-medium', 'Moyenne'),
        ('2-high', 'Élevée'),
        ('1-highest', 'Trés élevée'),
    ]
    CATEGORY_CHOICES = [
        ('01-organisation', 'Organisation'),
        ('02-compta', 'Compta'),
        ('03-achat', 'Achats'),
        ('04-sport', 'Sport'),
        ('05-sante', 'Santé'),
        ('06-contact', 'Contact'),
        ('07-informatique', 'Informatique'),
        ('08-menage', 'Menage'),
        ('09-jardin', 'Jardin'),
        ('10-doudou', 'Doudou'),
        ('11-bricoles', 'Bricoles'),
        ('12-couture', 'Couture'),
        ('13-loisirs', 'Loisirs'),
    ]
    WHO_CHOICES = [
        ('SLB', 'Sylvie'),
        ('JCB', 'Jean-Christophe'),
        ('LAU', 'Laurine'),
        ('THO', 'Thomas'),
        ('ODI', 'Odile'),
    ]
    PLACE_CHOICES = [
        ('cantin', 'Cantin'),
        ('chm', 'CHM'),
        ('genese', 'Genèse'),
        ('partout', 'Partout'),
    ]
    PERIODIC_CHOICES = [
        ('01-none', 'une seule fois'),
        ('02-everyday', 'Tous les jours'),
        ('03-every2days', 'Tous les 2 jours'),
        ('04-every3days', 'Tous les 3 jours'),
        ('05-every4days', 'Tous les 4 jours'),
        ('06-every5days', 'Tous les 5 jours'),
        ('07-everyweek', 'Toutes les semaines'),        
        ('08-every10days', 'Tous les 10 jours'),
        ('09-every2weeks', 'Toutes les 2 semaines'),
        ('10-everymonth', 'Tous les mois'),
        ('11-every6weeks', 'Toutes les 6 semaines'),
        ('12-every2months', 'Tous les 2 mois'),
        ('13-every3months', 'Tous les 3 mois'),
        ('14-every4months', 'Tous les 4 mois'),
        ('15-every6months', 'Tous les 6 mois'),
        ('16-everyyear', 'Tous les ans'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='todo')
    duration = models.DurationField(blank=True, null=True)
    description = models.TextField()
    appointment = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='01-organisation')
    who = models.CharField(max_length=20, choices=WHO_CHOICES, default='SLB')
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default='partout')
    periodic = models.CharField(max_length=20, choices=PERIODIC_CHOICES, default='partout')
    date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='01-none')
    done = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description
