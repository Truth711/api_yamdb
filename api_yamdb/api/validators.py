from django.core.exceptions import ValidationError


def validate_name(username):
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя.')
