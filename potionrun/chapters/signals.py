from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Act, Chapter, Scene


@receiver(post_save, sender=Chapter)
def update_chapter_stats(sender, instance, created, **kwargs):
    """Met à jour les statistiques du chapitre"""
    if created:
        # Créer les 7 actes par défaut
        for i in range(1, 8):
            Act.objects.create(chapter=instance, number=i)


@receiver(post_save, sender=Act)
def update_act_stats(sender, instance, created, **kwargs):
    if created:
        # Création des scènes par défaut
        for i in range(1, 4):
            Scene.objects.create(act=instance, number=i, instructions=f"Scène {i} par défaut")
