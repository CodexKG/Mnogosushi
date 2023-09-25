# Generated by Django 4.2.5 on 2023-09-25 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название сайта')),
                ('description', models.TextField(blank=True, max_length=400, null=True, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/', verbose_name='Логотип')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес')),
                ('facebook', models.URLField(blank=True, null=True, verbose_name='Facebook')),
                ('instagram', models.URLField(blank=True, null=True, verbose_name='Instagram')),
                ('tiktok', models.URLField(blank=True, null=True, verbose_name='TikTok')),
                ('whatsapp', models.URLField(blank=True, null=True, verbose_name='WhatsApp')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
