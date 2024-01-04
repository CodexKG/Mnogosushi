from django.db import models
from django.contrib.auth import get_user_model

from apps.categories.models import Category

User = get_user_model()

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
    iiko_image = models.CharField(
        max_length=500,
        verbose_name="Фотография Iiko",
        blank=True, null=True
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

class ReviewProduct(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='users_review',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_reviews",
        verbose_name="Товар"
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Сообщение"
    )
    stars = models.SmallIntegerField(
        verbose_name="Звезды",
        help_text="Отзывы от 1 до 5"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"