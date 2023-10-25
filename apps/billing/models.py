from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid

from apps.products.models import Product

# Create your models here.
class Billing(MPTTModel):
    billing_receipt_type = models.CharField(
        max_length=100,
        default='Самовывоз',
        verbose_name=('Вид получения товара')
    )
    total_price = models.PositiveIntegerField(
        verbose_name="Итоговая цена товаров",
    )
    address = models.CharField(
        max_length=300,
        verbose_name="Адрес доставки"
    )
    phone = models.CharField(
        max_length=200,
        verbose_name="Номер телефона"
    )
    payment_method = models.CharField(
        max_length=100,
        verbose_name="Способ оплаты",
        default="Наличные"
    )
    payment_code = models.CharField(
        max_length=20, unique=True,
        verbose_name="Код оплаты биллинга",
    )
    status = models.BooleanField(
        default=False, verbose_name="Статус заказа"
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания биллинга"
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.billing_receipt_type} {self.payment_code}"
    
    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = str(uuid.uuid4().int)[:20]  # Генерируем UUID и оставляем только первые 20 цифр
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Биллинг"
        verbose_name_plural = "Биллинги"

class BillingProduct(models.Model):
    billing = TreeForeignKey(Billing, on_delete=models.CASCADE, related_name='billing_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество товаров")
    price = models.PositiveBigIntegerField(verbose_name="Итоговая цена", default=0)
    status = models.BooleanField(verbose_name="Статус", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.billing} - {self.product} ({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Продукт биллинга"
        verbose_name_plural = "Продукты биллингов"
        
class SaleSummary(Billing):
    class Meta:
        proxy = True
        verbose_name = 'Отчет продажа товар'
        verbose_name_plural = 'Отчеты продажи товаров'

class BillingMenu(MPTTModel):
    total_price = models.PositiveIntegerField(
        verbose_name="Итоговая цена товаров",
    )
    payment_method = models.CharField(
        max_length=100,
        verbose_name="Способ оплаты",
        default="Наличные"
    )
    payment_code = models.CharField(
        max_length=20, unique=True,
        verbose_name="Код оплаты биллинга",
    )
    status = models.BooleanField(
        default=False, verbose_name="Статус заказа"
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания биллинга"
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.billing_receipt_type} {self.payment_code}"
    
    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = str(uuid.uuid4().int)[:20]  # Генерируем UUID и оставляем только первые 20 цифр
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Биллинг (Menu)"
        verbose_name_plural = "Биллинги (Menu)"

class BillingMenuProduct(models.Model):
    billing = TreeForeignKey(BillingMenu, on_delete=models.CASCADE, related_name='billing_menu_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество товаров")
    price = models.PositiveBigIntegerField(verbose_name="Итоговая цена", default=0)
    status = models.BooleanField(verbose_name="Статус", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.billing} - {self.product} ({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Продукт биллинга"
        verbose_name_plural = "Продукты биллингов"