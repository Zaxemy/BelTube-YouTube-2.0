from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.CharField(max_length=2000, blank=True, null=True)
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
    def __str__(self):
        return self.username
  
