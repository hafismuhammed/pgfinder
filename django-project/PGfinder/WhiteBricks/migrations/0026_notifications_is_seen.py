# Generated by Django 3.0.7 on 2020-09-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0025_auto_20200830_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
