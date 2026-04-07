from datetime import datetime
from enum import Enum
from django.utils import timezone

from .. import constants

def format_number(value):
    try:
        return f"{float(value):,.2f}".replace(',', '.')
    except (ValueError, TypeError):
        return "—"

def format_text(value):
    try:
        return str(value)
    except (ValueError, TypeError):
        return "—"

def format_date(value: datetime):
    try:
        return value.strftime(constants.DATE_FORMAT)
    except (ValueError, TypeError):
        return "—"

def format_datetime(value):
    try:
        return timezone.localtime(value).strftime(constants.DATETIME_FORMAT)
    except (ValueError, TypeError):
        return "—"