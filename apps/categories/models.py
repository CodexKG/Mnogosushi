from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    slug = models.SlugField(
        verbose_name="Slug"
    )
    external_id = models.CharField(max_length=255, unique=True, null=True, verbose_name="Внешний ID")

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"