# Generated by Django 4.2.7 on 2024-03-14 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_reciver',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]