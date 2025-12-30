from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # email = models.EmailField()
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Avatar')


    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username