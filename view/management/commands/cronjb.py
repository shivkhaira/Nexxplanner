from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.http import HttpResponse


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("K")
