from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
import multiprocessing

from view.models import Insta,Iupload
from view.autobot import Int
from view.instabot import Bot
class Command(BaseCommand):

    def handle(self, *args, **options):
        p = Insta.objects.get(id=1)
        multiprocessing.Process(target=Int.up, args=(p.username, p.password, 'media/' + img, data.caption)).start()
        print(p.file)
        subject = p.caption
        message = 'Hi , thank you for registering in geeksforgeeks.'
        email_from = "shivsinghkhaira@gmail.com"
        recipient_list = ['shivsinghkhaira@gmail.com']
        #send_mail(subject, message, email_from, recipient_list)


