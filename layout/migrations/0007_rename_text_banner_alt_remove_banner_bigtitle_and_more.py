# Generated by Django 4.2.7 on 2024-03-07 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0006_alter_banner_for_what'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='text',
            new_name='alt',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='bigTitle',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='button',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='color_title',
        ),
    ]
