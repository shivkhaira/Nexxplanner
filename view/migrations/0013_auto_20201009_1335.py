# Generated by Django 3.1.1 on 2020-10-09 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0012_auto_20201009_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iupload',
            name='caption',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='iupload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 13, 35, 47, 1077)),
        ),
    ]
