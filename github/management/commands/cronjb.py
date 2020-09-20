from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from ....view.instabot import Bot


class Command(BaseCommand):

    def handle(self, *args, **options):


        requests.post(
            "http://bulksms.samvestor.com/app/smsapi/index.php?key=35E8A0D2830519&campaign=0&routeid=9&type=text&contacts=8847469407&senderid=AARAMP&msg=Hello")


        subject = 'welcome to GFG world'
        message = 'Hi , thank you for registering in geeksforgeeks.'
        email_from = "shivsinghkhaira@gmail.com"
        recipient_list = ['shivsinghkhaira@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
