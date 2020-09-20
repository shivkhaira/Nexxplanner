from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests


from view.models import Insta

class Command(BaseCommand):

    def handle(self, *args, **options):
        p = Insta.objects.get(id=1)
        subject = p.username
        message = 'Hi , thank you for registering in geeksforgeeks.'
        email_from = "shivsinghkhaira@gmail.com"
        recipient_list = ['shivsinghkhaira@gmail.com']
        send_mail(subject, message, email_from, recipient_list)


