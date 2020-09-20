from django.conf import settings

from django.core.mail import send_mail
import os
import requests

from .models import Pro,Insta,Iupload
settings.configure()


name=Insta.objects.get(id=1)
subject = 'welcome to GFG world '+name.username
message = 'Hi , thank you for registering in geeksforgeeks.'
email_from = "shivsinghkhaira@gmail.com"
recipient_list = ['shivsinghkhaira@gmail.com']
send_mail(subject, message, email_from, recipient_list)