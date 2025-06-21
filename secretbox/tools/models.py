from django.utils import timezone
from datetime import date, timedelta, datetime
import random

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
    random_day = random.randint(1, last_day_of_month.day)
    random_date = date(year, month, random_day)

    # Convert in django timezone
    # random_date = datetime.combine(random_date, )
    random_date = datetime.combine(random_date, datetime.min.time())
    random_date = timezone.make_aware(random_date)
    # random_date = random_date.astimezone(timezone.get_current_timezone())
    return random_date