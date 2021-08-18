from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    USER = 'user', _('Пользователь')
    MODERATOR = 'moderator', _('Модератор')
    ADMIN = 'admin', _('Админ')


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-id']

    @property
    def is_admin(self):
        return (
            self.role == Role.ADMIN
            and self.is_active
            or self.is_active
            and self.is_superuser
        )

    @property
    def is_moderator(self):
        return (
            self.role == Role.MODERATOR
            and self.is_active
        )

    def __str__(self):
        return self.username
