# Generated by Django 4.2.5 on 2023-11-16 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='SKU'),
        ),
    ]
