# Generated by Django 4.2.5 on 2023-09-27 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0010_billing_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='payment_method',
            field=models.CharField(default='Наличные', max_length=100, verbose_name='Способ оплаты'),
        ),
    ]
