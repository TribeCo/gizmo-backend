# Generated by Django 4.2.7 on 2024-04-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productcolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolor',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
