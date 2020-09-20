from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from ....view.instabot import Bot

from ....view.models import Pro,Insta,Iupload

class Command(BaseCommand):

    def handle(self, *args, **options):

        name = Insta.objects.all()[0]
        print(name['username'])

        subject = name
        message = 'Hi , thank you for registering in geeksforgeeks.'
        email_from = "shivsinghkhaira@gmail.com"
        recipient_list = ['shivsinghkhaira@gmail.com']
        send_mail(subject, message, email_from, recipient_list)


