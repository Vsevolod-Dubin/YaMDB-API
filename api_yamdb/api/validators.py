from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year(year):
    if year < 0 or year > datetime.now().year:
        raise ValidationError(
            'Год недействителен!'
        )
