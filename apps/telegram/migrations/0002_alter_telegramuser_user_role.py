# Generated by Django 4.2.5 on 2023-11-22 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_telegram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='user_role',
            field=models.CharField(choices=[('User', 'Пользователь'), ('Delivery', 'Курьер'), ('Manager', 'Менеджер'), ('Waiter', 'Официант')], default='Пользователь', max_length=100, verbose_name='Роль пользователя'),
        ),
    ]