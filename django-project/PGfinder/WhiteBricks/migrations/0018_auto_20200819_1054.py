# Generated by Django 3.0.7 on 2020-08-19 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0017_auto_20200817_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='types',
            field=models.CharField(choices=[('family', 'family'), ('boys', 'boys'), ('girls', 'girls'), ('any', 'any')], max_length=100, null=True),
        ),
    ]
