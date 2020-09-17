from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os

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

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=40)
    gender = models.CharField(max_length=30,default='F')
    pic = models.ImageField(upload_to=file_change,default='images/image.png')
    activated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Insta(models.Model):


    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

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



