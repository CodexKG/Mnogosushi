# Generated by Django 4.2.5 on 2024-01-04 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_product_iiko_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Сообщение')),
                ('stars', models.SmallIntegerField(help_text='Отзывы от 1 до 5', verbose_name='Звезды')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='products.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_review', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
