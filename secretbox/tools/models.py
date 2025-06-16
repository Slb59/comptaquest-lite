from django.utils import timezone


def get_now_date():
    return timezone.now().date()
