# Generated by Django 3.0.7 on 2021-01-08 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0027_auto_20201026_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='visitors',
        ),
    ]
