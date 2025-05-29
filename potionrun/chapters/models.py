# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _



class Chapter(models.Model):
    name = models.CharField(_("Nom"), max_length=100)
    description = models.TextField(_("Description/Objectif"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Champs calculés (à mettre à jour via signaux ou méthodes)
    completed_sessions = models.PositiveIntegerField(
        _("Séances réalisées"),
        default=0
    )
    associated_routes = models.PositiveIntegerField(
        _("Parcours associés"),
        default=0
    )

    class Meta:
        verbose_name = _("Chapitre")
        verbose_name_plural = _("Chapitres")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chapter-detail', kwargs={'pk': self.pk})

class Act(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='acts',
        verbose_name=_("Chapitre")
    )
    number = models.PositiveSmallIntegerField(
        _("Numéro"),
        choices=[(i, f"Acte {i}") for i in range(1, 8)]
    )
    short = models.TextField(
        _("Titre"),
        blank=True
    )
    description = models.TextField(
        _("Description"),
        blank=True
    )

    class Meta:
        verbose_name = _("Acte")
        verbose_name_plural = _("Actes")
        ordering = ['chapter', 'number']
        unique_together = ('chapter', 'number')

    def __str__(self):
        return f"Acte {self.number} - {self.short}"

class Scene(models.Model):
    act = models.ForeignKey(
        Act,
        on_delete=models.CASCADE,
        related_name='scenes',
        verbose_name=_("Acte")
    )
    number = models.PositiveSmallIntegerField(
        _("Numéro"),
        choices=[(i, f"Scène {i}") for i in range(1, 4)]
    )
    short = models.TextField(
        _("Titre"),
        blank=True
    )

    instructions = models.TextField(
        _("Instructions"),
        help_text="Format: => Instruction 1\n=> Instruction 2"
    )

    class Meta:
        verbose_name = _("Scène")
        verbose_name_plural = _("Scènes")
        ordering = ['act', 'number']
        unique_together = ('act', 'number')

    def __str__(self):
        return f"Scène {self.number} - {self.short}"

    def get_instructions_list(self):
        """Retourne les instructions sous forme de liste"""
        return [instruction.strip() for instruction in self.instructions.split('\n') if instruction.strip()]

