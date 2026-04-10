from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """User model for storing user account information."""

    photo = models.ImageField(upload_to="user_photos/%Y/%m/%d", blank=True, null=True, verbose_name="Фото профиля")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return str(self.username)
