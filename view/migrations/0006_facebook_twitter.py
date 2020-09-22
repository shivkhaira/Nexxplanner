# Generated by Django 3.1.1 on 2020-09-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0005_insta_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('user', models.CharField(default='None', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumer_key', models.CharField(max_length=200)),
                ('consumer_secret', models.CharField(max_length=200)),
                ('access_token', models.CharField(max_length=200)),
                ('access_token_secret', models.CharField(max_length=200)),
                ('user', models.CharField(default='None', max_length=50)),
            ],
        ),
    ]