# Generated by Django 3.1.1 on 2020-10-02 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0003_auto_20200926_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iupload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 2, 16, 53, 50, 63485)),
        ),
    ]
