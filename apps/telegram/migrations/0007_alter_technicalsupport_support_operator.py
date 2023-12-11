# Generated by Django 4.2.5 on 2023-12-11 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_telegram', '0006_alter_technicalsupport_support_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicalsupport',
            name='support_operator',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_role': 'Manager'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_operator_user', to='my_telegram.telegramuser', verbose_name='Оператор поддержки'),
        ),
    ]
