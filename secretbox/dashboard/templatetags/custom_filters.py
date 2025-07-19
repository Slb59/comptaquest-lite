import locale

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def format_title(value):
    if isinstance(value, timezone.datetime):
        # Définir la locale à français
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        # Formatez la date selon vos besoins
        return value.strftime("%A %d %B %Y")
    return value

@register.filter
def can_edit_any(todo, user):
    return todo.can_edit_any(user)

@register.filter
def can_delete(todo, user):
    return todo.can_delete(user)
