import secrets
from datetime import date, datetime, timedelta

from django.utils import timezone


def get_now_date():
    return date.today()


def get_random_date_in_current_month():
    today = date.today()
    year = today.year
    month = today.month

    # Determine the last day of the current month
    if month == 12:
        next_month = 1
        next_month_year = year + 1
    else:
        next_month = month + 1
        next_month_year = year

    last_day_of_month = date(next_month_year, next_month, 1) - timedelta(days=1)

    # Generate a random day within the current month
    random_day = secrets.randbelow(last_day_of_month.day) + 1
    random_date = date(year, month, random_day)

    # Convert in django timezone and return

    return convert_date_to_django_date(random_date)


def convert_date_to_django_date(the_date):
    # Convert the date in django timezone
    the_date = datetime.combine(the_date, datetime.min.time())
    the_date = timezone.make_aware(the_date)
    return the_date
