from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    image = models.ImageField(
        upload_to='category_image/',
        verbose_name="Фотография категории",
        blank=True, null=True
    )
    iiko_image = models.CharField(
        max_length=500,
        verbose_name="Фотография Iiko",
        blank=True, null=True
    )
    slug = models.SlugField(
        verbose_name="Slug"
    )
    external_id = models.CharField(max_length=255, unique=True, null=True, verbose_name="Внешний ID")

    priority = models.IntegerField(verbose_name="Приоритет категории", default=0)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"