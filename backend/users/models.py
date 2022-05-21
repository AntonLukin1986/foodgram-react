from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return (
            f'Ник: {self.username} | '
            f'Почта: {self.email} | '
            f'Имя: {self.first_name} | '
            f'Фамилия: {self.last_name} | '
        )
