# Generated by Django 3.0.7 on 2020-08-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteBricks', '0022_auto_20200826_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='image1',
            field=models.FileField(null=True, upload_to='media/uploads'),
        ),
        migrations.AddField(
            model_name='property',
            name='image2',
            field=models.FileField(null=True, upload_to='media/uploads'),
        ),
    ]