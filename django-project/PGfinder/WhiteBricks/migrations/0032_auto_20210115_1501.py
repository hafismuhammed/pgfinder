# Generated by Django 3.0.7 on 2021-01-15 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WhiteBricks', '0031_propertyimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyimages',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='propertyimages',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WhiteBricks.Property'),
        ),
    ]