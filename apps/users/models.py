from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to='user_images/',
        verbose_name='Фотография профиля',
        default='no_image.jpg',
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        blank=True, null=True
    )
    
    def __str__(self):
        return self.username 
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"