# Generated by Django 4.2.7 on 2024-03-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0012_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqgroup',
            name='icon',
            field=models.ImageField(default=1, upload_to='media/faqs/pictures/'),
            preserve_default=False,
        ),
    ]