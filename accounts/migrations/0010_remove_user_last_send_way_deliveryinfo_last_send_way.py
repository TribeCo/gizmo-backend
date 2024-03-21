# Generated by Django 4.2.7 on 2024-03-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_deliveryinfo_user_delivery_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_send_way',
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='last_send_way',
            field=models.CharField(choices=[('c', 'درون شهری'), ('b', 'اتوبوس'), ('p', 'پست معمولی'), ('t', 'تیپاکس (پس کرایه)')], default='t', max_length=1),
        ),
    ]