from django.db import models
from apps.categories.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category_products",
        blank=True, null=True
    )
    title = models.CharField(
        max_length=300,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True, null=True
    )
    price = models.CharField(
        max_length=100,
        verbose_name="Цена"
    )
    image = models.ImageField(
        max_length=1000,
        verbose_name="Фотография продукта",
        default='no_image.jpg'
    )
    sku = models.CharField(max_length=255, unique=True, null=True, verbose_name="SKU")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"