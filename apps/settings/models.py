from django.db import models

# Create your models here.
class Setting(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название сайта"
    )
    description = models.TextField(
        max_length=400,
        verbose_name="Описание",
        blank=True, null=True
    )
    logo = models.ImageField(
        upload_to='logo/',
        verbose_name="Логотип",
        blank=True, null=True
    )
    mobile_logo = models.ImageField(
        upload_to='logo/',
        verbose_name="Мобильное лого",
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Почта",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        blank=True, null=True
    )
    address = models.CharField(
        max_length=300,
        verbose_name="Адрес",
        blank=True, null=True
    )
    facebook = models.URLField(
        verbose_name="Facebook",
        blank=True, null=True
    )
    instagram = models.URLField(
        verbose_name="Instagram",
        blank=True, null=True
    )
    tiktok = models.URLField(
        verbose_name="TikTok",
        blank=True, null=True
    )
    telegram = models.URLField(
        verbose_name="Telegram",
        blank=True, null=True
    )
    whatsapp = models.URLField(
        verbose_name="WhatsApp",
        blank=True, null=True
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона"
    )
    message = models.CharField(
        max_length=500,
        verbose_name="Сообщение",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

class Statistics(models.Model):
    count_visits = models.IntegerField(
        default=0,
        verbose_name="Количество посещений сайта (Главная)"
    )
    count_visits_menu = models.IntegerField(
        default=0,
        verbose_name="Количество посещений сайта (Меню)"
    )
    
    def __str__(self):
        return f"{self.count_visits} {self.count_visits_menu}"
    
    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"