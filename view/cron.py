from django.core.mail import send_mail

def cron_job():
    send_mail("hello paul", "hello", "shivsinghkhaira@gmail.com", ['shivsinghkhaira@gmail.com'])
