# Generated by Django 3.0.7 on 2020-08-26 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0020_remove_property_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='types',
            field=models.CharField(choices=[('family', 'Family'), ('boys', 'Boys'), ('girls', 'Girls'), ('any', 'any')], max_length=100, null=True),
        ),
    ]