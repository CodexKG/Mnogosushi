# Generated by Django 4.2.5 on 2024-03-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_billing_delivery_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу'),
        ),
    ]
