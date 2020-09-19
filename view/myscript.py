from django.core.mail import send_mail



def handle():
    subject = 'welcome to GFG world'
    message = 'Hi , thank you for registering in geeksforgeeks.'
    email_from = "shivsinghkhaira@gmail.com"
    recipient_list = ['shivsinghkhaira@gmail.com']
    send_mail(subject, message, email_from, recipient_list)