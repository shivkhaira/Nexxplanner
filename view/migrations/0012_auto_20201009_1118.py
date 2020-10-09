# Generated by Django 3.1.1 on 2020-10-09 05:48

import datetime
from django.db import migrations, models
import view.models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0011_auto_20201004_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iupload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 11, 18, 2, 668847)),
        ),
        migrations.AlterField(
            model_name='iupload',
            name='file',
            field=models.ImageField(default='null', upload_to=view.models.Iupload.file_change),
        ),
    ]
