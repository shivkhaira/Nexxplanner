# Generated by Django 3.1.1 on 2020-12-09 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0013_auto_20201009_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro',
            name='limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='iupload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 9, 14, 22, 3, 236416)),
        ),
    ]
