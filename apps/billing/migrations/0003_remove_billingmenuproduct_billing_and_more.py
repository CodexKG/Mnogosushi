# Generated by Django 4.2.5 on 2023-11-01 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_billingmenu_billingmenuproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingmenuproduct',
            name='billing',
        ),
        migrations.RemoveField(
            model_name='billingmenuproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='BillingMenu',
        ),
        migrations.DeleteModel(
            name='BillingMenuProduct',
        ),
    ]
