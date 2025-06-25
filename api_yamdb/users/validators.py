import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя "me" запрещено.')

    invalid_chars = re.sub(r'[\w.@+-]', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Недопустимые символы: {", ".join(sorted(set(invalid_chars)))}'
        )
