from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from users.validators import validate_username


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLE_CHOICES = (
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    )

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
        verbose_name='Имя пользователя',
        help_text=('Обязательное. Только буквы, цифры и '
                   '@/./+/-/_. Имя "me" запрещено.')
    )
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус сотрудника',

    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = self.role == self.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
