# Generated by Django 4.2.7 on 2024-04-06 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_available_remove_product_warehouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
    ]