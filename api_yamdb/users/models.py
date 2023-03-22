from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(choices=ROLES,
                            default=USER,
                            max_length=25,
                            blank=True)
    confirmation_code = models.CharField(max_length=250)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
