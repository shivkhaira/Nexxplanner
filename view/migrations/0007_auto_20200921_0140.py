# Generated by Django 3.1.1 on 2020-09-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0006_facebook_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='iupload',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='iupload',
            name='users',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
