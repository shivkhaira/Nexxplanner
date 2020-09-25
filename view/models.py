from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os
from datetime import datetime
# Create your models here.

class Pro(models.Model):
    def file_change(instance, filename):
        upload_to = 'images/'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file

        return os.path.join(upload_to, filename)

    user = models.CharField(max_length=40)
    pic = models.ImageField(upload_to=file_change,default='images/image.png')
    activated = models.BooleanField(default=False)
    instagram=models.BooleanField(default=False)
    facebook=models.BooleanField(default=False)
    twitter=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Insta(models.Model):


    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    user=models.CharField(max_length=50,default='None')


    def __str__(self):
        return str(self.user)

class Facebook(models.Model):


    token=models.CharField(max_length=1000)
    page_id=models.CharField(max_length=100,default=0)
    user=models.CharField(max_length=50,default='None')


    def __str__(self):
        return str(self.user)

class Twitter(models.Model):


    consumer_key=models.CharField(max_length=200)
    consumer_secret=models.CharField(max_length=200)
    access_token=models.CharField(max_length=200)
    access_token_secret=models.CharField(max_length=200)
    username=models.CharField(max_length=100,default='admin')
    user=models.CharField(max_length=50,default='None')


    def __str__(self):
        return str(self.user)


class Iupload(models.Model):

    def file_change(instance, filename):
        upload_to = 'images/'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file

        return os.path.join(upload_to, filename)

    file=models.ImageField(upload_to=file_change)
    caption=models.CharField(max_length=250)
    instagram=models.BooleanField(default=False)
    facebook=models.BooleanField(default=False)
    twitter=models.BooleanField(default=False)
    users=models.CharField(max_length=50,default='None')
    done=models.BooleanField(default=False)

    def __str__(self):
        return str(self.users)+str(self.id)

class Save(models.Model):
    ndate=models.DateTimeField(default=datetime.now)
    sdate=models.DateField(default=datetime.now)
    stime=models.TimeField(default=datetime.now)
    fid=models.IntegerField(default=0)
    user=models.CharField(max_length=50,default='admin')
    done=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


