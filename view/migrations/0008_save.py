# Generated by Django 3.1.1 on 2020-09-21 07:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0007_auto_20200921_0140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ndate', models.DateTimeField(default=datetime.datetime(2020, 9, 21, 12, 30, 51, 237013))),
                ('sdate', models.DateTimeField()),
                ('fid', models.IntegerField()),
            ],
        ),
    ]