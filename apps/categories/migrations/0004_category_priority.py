# Generated by Django 4.2.5 on 2023-12-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_iiko_image_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='priority',
            field=models.IntegerField(default=0, verbose_name='Приоритет категории'),
        ),
    ]