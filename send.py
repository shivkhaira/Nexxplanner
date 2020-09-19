from django.conf import settings
from django.core.mail import send_mail
import os
import requests

api = requests.post(
    "http://bulksms.samvestor.com/app/smsapi/index.php?key=35E8A0D2830519&campaign=0&routeid=9&type=text&contacts=8847469407&senderid=AARAMP&msg=Hello")

if __name__ == '__main__' and __package__ is None:
    os.sys.path.append(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "github.settings")

subject = 'welcome to GFG world'
message = 'Hi , thank you for registering in geeksforgeeks.'
email_from = "shivsinghkhaira@gmail.com"
recipient_list = ['shivsinghkhaira@gmail.com']
send_mail(subject, message, email_from, recipient_list)