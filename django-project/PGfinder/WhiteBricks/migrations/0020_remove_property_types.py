# Generated by Django 3.0.7 on 2020-08-26 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0019_property_deposite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='types',
        ),
    ]
