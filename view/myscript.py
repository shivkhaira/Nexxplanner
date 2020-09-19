


def handle():
    from django.core.mail import send_mail
    import os
    from django.conf import settings

    if __name__ == '__main__' and __package__ is None:
        os.sys.path.append(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "github.github.settings")

    subject = 'welcome to GFG world'
    message = 'Hi , thank you for registering in geeksforgeeks.'
    email_from = "shivsinghkhaira@gmail.com"
    recipient_list = ['shivsinghkhaira@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    
