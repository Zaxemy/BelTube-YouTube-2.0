from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=2000, blank=True, null=True)
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)
    subscribers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='subscriptions',
        blank=True,
        verbose_name='Подписчики'
    )

    @property
    def subscribers_count(self):
        return self.subscribers.count()

    @property
    def subscriptions_count(self):
        return self.subscriptions.count()