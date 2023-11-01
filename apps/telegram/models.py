from django.db import models

from apps.billing.models import Billing

# Create your models here.
class TelegramUser(models.Model):
    USER_ROLE_CHOICE = (
        ('User', 'Пользователь'),
        ('Delivery', 'Курьер'),
        ('Manager', 'Менеджер')
    )
    username = models.CharField(
        max_length=200, verbose_name="Имя пользователя",
        blank=True, null=True
    )
    user_id = models.CharField(
        max_length=200,
        verbose_name="ID пользователя telegram"
    )
    first_name = models.CharField(
        max_length=200, verbose_name="Имя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=200, verbose_name="Фамилия",
        blank=True, null=True
    )
    user_role = models.CharField(
        max_length=100,
        choices=USER_ROLE_CHOICE,
        verbose_name="Роль пользователя",
        default="Пользователь"
    )
    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания",
    )

    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        verbose_name = "Телеграм пользователь"
        verbose_name_plural = "Телеграм пользователи"

class BillingDelivery(models.Model):
    STATUS_DELIVERY_CHOICE = (
        ('Accepted', 'Принят'),
        ('On way', 'В пути'),
        ('Delivered', 'Доставлен'),
        ('Cancel', 'Отменен')
    )
    billing = models.ForeignKey(
        Billing, on_delete=models.SET_NULL,
        verbose_name="Биллинг", null=True
    )
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.SET_NULL,
        verbose_name="Пользователь", null=True
    )
    delivery = models.CharField(
        max_length=100,
        choices=STATUS_DELIVERY_CHOICE,
        verbose_name="Статус доставки",
        default="Принят"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.billing}"
    
    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"

class BillingDeliveryHistory(models.Model):
    delivery = models.ForeignKey(
        BillingDelivery, on_delete=models.CASCADE,
        related_name='delivery_history',
        verbose_name="Доставка"
    )
    message = models.CharField(
        max_length=200,
        verbose_name="Сообщение"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время"
    )

    def __str__(self):
        return f"{self.created}"
    
    class Meta:
        verbose_name = "История доставки"
        verbose_name_plural = "История доставок"