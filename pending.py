from django.conf import settings

import os

def pp():
    from datetime import datetime
    from view.models import Insta, Iupload, Save, Twitter, Facebook, LinkD
    import multiprocessing
    from view.autobot import Int

    curr = (datetime.now())
    pending = Save.objects.filter(done=False)
    for i in pending:
        dt = datetime.combine(i.sdate, i.stime)
        if curr >= dt:
            data = Iupload.objects.get(id=i.fid)
            if data.linkd:
                fb = LinkD.objects.get(profile=i.profile)
                token = fb.access_token
                urn = fb.urn
                multiprocessing.Process(target=Int.linkd,
                                        args=(token, urn, 'media/' + str(data.file), data.caption)).start()
            if data.facebook:
                face = Facebook.objects.get(profile=i.profile)
                token = face.token
                page_id = face.page_id
                multiprocessing.Process(target=Int.face,
                                        args=(token, page_id, 'media/' + str(data.file), data.caption)).start()
            if data.twitter:
                twit = Twitter.objects.get(profile=i.profile)
                consumer_key = twit.consumer_key
                consumer_secret = twit.consumer_secret
                access_token = twit.access_token
                access_token_secret = twit.access_token_secret
                multiprocessing.Process(target=Int.twit, args=(
                    consumer_key, consumer_secret, access_token, access_token_secret, 'media/' + str(data.file),
                    data.caption)).start()
            if data.instagram:
                insta = Insta.objects.get(profile=i.profile)
                username = insta.username
                password = insta.password
                multiprocessing.Process(target=Int.up,
                                        args=(username, password, 'media/' + str(data.file), data.caption)).start()
            yep = Save.objects.get(id=i.id)
            qte = Iupload.objects.get(id=i.fid)
            qte.done = True
            qte.save()
            yep.done = True
            yep.save()
def main():
    os.sys.path.append(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "github.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()
    pp()


if __name__ == '__main__' and __package__ is None:


    main()
