# Generated by Django 3.0.7 on 2020-08-17 14:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WhiteBricks', '0014_profile_verify_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='type',
            field=models.CharField(choices=[('Family', 'Family'), ('Boys', 'Boys'), ('Girls', 'Girls'), ('Any', 'Any')], default='Any', max_length=100),
        ),
        migrations.AlterField(
            model_name='property',
            name='notify',
            field=models.ManyToManyField(blank=True, default=None, related_name='notify', to=settings.AUTH_USER_MODEL),
        ),
    ]