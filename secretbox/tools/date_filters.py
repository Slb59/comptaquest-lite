from django import template
from datetime import datetime

register = template.Library()

@register.filter
def parse_iso_date(value):
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return value