from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import multiprocessing
from datetime import datetime
from ....view.models import Pro,Insta,Iupload,Save,Twitter,Facebook
from ....view.autobot import Int
class Command(BaseCommand):

    def handle(self, *args, **options):
        subject = 'welcome to GFG world'
        message = 'Mangno'
        email_from = 'shivsinghkhaira@gmail.com'
        recipient_list = ['shivsinghkhaira@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)
        print("gdbd")
        curr = (datetime.now())
        pending = Save.objects.filter(done=False)
        for i in pending:
            print("in")
            dt = datetime.combine(i.sdate, i.stime)
            if curr >= dt:
                insta = Insta.objects.get(user=i.user)
                face = Facebook.objects.get(user=i.user)
                twit = Twitter.objects.get(user=i.user)
                username = insta.username
                password = insta.password
                token = face.token
                consumer_key = twit.consumer_key
                consumer_secret = twit.consumer_secret
                access_token = twit.access_token
                access_token_secret = twit.access_token_secret
                id=i.fid
                data=Iupload.objects.get(id=id)
                if data.facebook:
                    multiprocessing.Process(target=Int.face,
                                            args=(token, 'media/' + str(data.file), data.caption)).start()
                if data.twitter:
                    multiprocessing.Process(target=Int.twit, args=(
                    consumer_key, consumer_secret, access_token, access_token_secret, 'media/' + str(data.file),
                    data.caption)).start()
                if data.instagram:
                    multiprocessing.Process(target=Int.up,
                                            args=(username, password, 'media/' + str(data.file), data.caption)).start()
                yep=Save.objects.get(id=i.id)
                yep.done=True
                yep.save()
            else:
                print(False)





