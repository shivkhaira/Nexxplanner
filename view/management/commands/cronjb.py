from django.core.management.base import BaseCommand
from django.core.mail import send_mail



class Command(BaseCommand):

    def handle(self, *args, **options):
        subject = 'welcome to GFG world'
        message = 'Hi , thank you for registering in geeksforgeeks.'
        email_from = "shivsinghkhaira@gmail.com"
        recipient_list = ['shivsinghkhaira@gmail.com']
        send_mail(subject, message, email_from, recipient_list)