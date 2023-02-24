from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if not (1700 < value <= timezone.now().year):
        raise ValidationError('Проверьте ещё не вышло!')
