from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from wsgiref.util import FileWrapper
import mimetypes
import threading
from django.contrib.auth.forms import AuthenticationForm
from .form import Finsta,Uinsta,Ureg,Face,Twit,Schedule,Customauth,SetProfie
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .autobot import Int
from .models import Insta,Iupload,Pro,Facebook,Twitter,Save,Insta_data,Profile,LinkD
import multiprocessing
from django.http import Http404
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse,JsonResponse
from datetime import date,datetime
import oauth2 as oauth
import requests
import tweepy
import magic
import urllib
# Create your views here.

@login_required
def home(request):
    if request.user.is_authenticated:
        return redirect('aws')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users')
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'index.html', {'form': form, 'active': 'login'})
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="index.html",
                  context={"form": form, 'active': 'login'})


def logind(request):
    if request.GET.get('next'):
        next = request.GET.get('next')
    else:
        next='/users/'
    if request.user.is_authenticated:
        return redirect('users')
    if request.method == 'POST':
        form = Customauth(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['profile']=None
                return JsonResponse({'status': str(request.user)})
            else:
                return JsonResponse({'status': 'no'})
        else:
            return JsonResponse({'status': 'no'})
    form = Customauth()
   
    return render(request, "login.html", {"form": form,'next':next})

@ login_required (login_url='/login/', redirect_field_name=None)
def logoutt(request):
        logout(request)
        return redirect("login")

def register(request):
    if request.user.is_authenticated:
        return  redirect('users')
    if request.method == 'POST':
        form = Ureg(request.POST)
        if form.is_valid():
            f=form.save()
            Pro.objects.create(user=f.username)
            messages.success(request, 'Account created successfully')
            return render(request, 'register.html', {'form': form,'register':1})
        else:
            return render(request, 'register.html', {'form': form})

    f = Ureg()
    return render(request, 'register.html', {'form': f,'active':'register'})

@login_required
def iupload(request):
    if request.method=='POST':
        form=Uinsta(request.POST,request.FILES)
        if len(request.FILES) == 0 and request.POST.get('instagram'):
            return render(request,'upload.html',{'form':form,'instap':'1'})
        if request.POST.get('twitter') and len(request.POST.get('caption'))>280:
            return render(request,'upload.html',{'form':form,'tlimit':'1'})
        if form.is_valid():
            insta = request.POST.get('instagram')
            face = request.POST.get('facebook')
            twit = request.POST.get('twitter')
            linkd = request.POST.get('linkd')
            if insta or face or twit or linkd:
                abb=1
            else:
                abb=0
            if abb==0:
                return render(request,'upload.html',{'form':form,'non_select':'1'})
            form.instance.users=request.user
            form.instance.done=True
            if insta:
                form.instance.instagram=True
            if face:
                form.instance.facebook=True
            if twit:
                form.instance.twitter=True
            if twit:
                form.instance.linkd=True

            form.instance.profile=request.session['profile']
            data=form.save()
            pic=Iupload.objects.get(id=data.id)

            img = str(pic.file)


            if linkd:
                fb = LinkD.objects.get(Q(user=request.user.username) & Q(profile=request.session['profile']))
                token = fb.access_token
                urn=fb.urn
                multiprocessing.Process(target=Int.linkd,
                                        args=(token,urn,'media/' + img, data.caption)).start()

            if face:
                fb = Facebook.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
                token = fb.token
                page_id=fb.page_id
                multiprocessing.Process(target=Int.face,
                                        args=(token,page_id,'media/' + img, data.caption)).start()
            if twit:
                tw = Twitter.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
                consumer_key = tw.consumer_key
                consumer_secret = tw.consumer_secret
                access_token = tw.access_token
                access_token_secret = tw.access_token_secret
                multiprocessing.Process(target=Int.twit, args=(consumer_key,consumer_secret,access_token,access_token_secret,'media/' + img, data.caption)).start()
            if insta:
                p = Insta.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
                multiprocessing.Process(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            #threading.Thread(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            return render(request,'upload.html',{'form':form,'uploaded':'1'})
        else:
            return redirect('home')
    data=Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
    if data.instagram:
        instagram=1
    else:
        instagram=0

    if data.facebook:
        facebook=1
    else:
        facebook=0

    if data.twitter:
        twitter=1
    else:
        twitter=0

    if data.linkd:
        linkd=1
    else:
        linkd=0

    all=instagram+facebook+twitter+linkd
    if all == 0:
        return redirect('users')

    return render(request,'upload.html',{'form':Uinsta()})

@login_required
def setup(request,name):
    if request.method=='POST':
        if name=='instagram':
            form=Finsta(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.profile = request.session['profile']
                form.save()
                rec=Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
                rec.instagram = True
                rec.save()
                if (Insta_data.objects.filter(Q(user=request.user) & Q(profile=request.session['profile']))).count()==0:
                    Insta_data.objects.create(user=request.user,profile=request.session['profile'])
                return redirect('aws')
        elif name=='facebook':
            form=Face(request.POST)
            if form.is_valid():
                form.instance.user=request.user
                form.instance.profile = request.session['profile']
                form.save()
                rec=Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
                rec.facebook=True
                rec.save()
                return redirect('aws')

    if name=='instagram':
        rec = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        if rec.instagram:
            return redirect('aws')
        else:
            return render(request,'setup.html',{'name':name,'form':Finsta()})
    elif name=='facebook':
        rec =Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        if rec.facebook:
            return redirect('aws')
        else:
            return render(request,'setup.html',{'name':name,'form':Face()})
    elif name=='twitter':
        rec =Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        if rec.twitter:
            return redirect('aws')
        else:
            return render(request,'setup.html',{'name':name,'form':Twit(),'social':'twitter'})
    elif name=='linkd':
        rec =Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        if rec.linkd:
            return redirect('aws')
        else:
            return render(request,'setup.html',{'name':name,'form':Twit(),'social':'linkd'})

@login_required
def sch(request):
    if request.method=='POST':
        form=Schedule(request.POST)
        uform=Uinsta(request.POST,request.FILES)
        if len(request.FILES) == 0 and request.POST.get('instagram'):
            return render(request,'schedule.html',{'form':uform,'form1':form,'instap':'1'})
        if request.POST.get('twitter') and len(request.POST.get('caption'))>280:
            return render(request,'schedule.html',{'form':uform,'form1':form,'tlimit':'1'})

        if form.is_valid() and uform.is_valid():
            insta = request.POST.get('instagram')
            face = request.POST.get('facebook')
            twit = request.POST.get('twitter')
            linkd = request.POST.get('linkd')
            if insta or face or twit or linkd:
                abb=1
            else:
                abb=0
            if abb==0:
                return render(request,'schedule.html',{'form':uform,'non_select':'1','form1':form})
            uform.instance.users = request.user
            if insta:
                uform.instance.instagram = True
            if face:
                uform.instance.facebook = True
            if twit:
                uform.instance.twitter = True
            if linkd:
                uform.instance.linkd = True
            uform.instance.profile = request.session['profile']
            data=uform.save()
            form.instance.fid=data.id
            form.instance.user=request.user
            form.instance.profile = request.session['profile']
            form.save()
            return render(request,'schedule.html',{'uploaded':'1','form':Uinsta(),'form1':Schedule()})
        else:
            return Http404
    data = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
    if data.instagram:
        instagram = 1
    else:
        instagram = 0

    if data.facebook:
        facebook = 1
    else:
        facebook = 0

    if data.twitter:
        twitter = 1
    else:
        twitter = 0

    if data.linkd:
        linkd = 1
    else:
        linkd = 0

    all = instagram + facebook + twitter + linkd
    if all == 0:
        return redirect('users')
    return render(request,'schedule.html',{'form':Uinsta(),'form1':Schedule()})

def check(request):
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
                page_id=face.page_id
                multiprocessing.Process(target=Int.face,args=(token,page_id, 'media/' + str(data.file), data.caption)).start()
            if data.twitter:
                twit = Twitter.objects.get(profile=i.profile)
                consumer_key = twit.consumer_key
                consumer_secret = twit.consumer_secret
                access_token = twit.access_token
                access_token_secret = twit.access_token_secret
                multiprocessing.Process(target=Int.twit, args=(consumer_key, consumer_secret, access_token, access_token_secret, 'media/' + str(data.file),data.caption)).start()
            if data.instagram:
                insta = Insta.objects.get(profile=i.profile)
                username = insta.username
                password = insta.password
                multiprocessing.Process(target=Int.up, args=(username, password, 'media/' + str(data.file), data.caption)).start()
            yep=Save.objects.get(id=i.id)
            qte=Iupload.objects.get(id=i.fid)
            qte.done=True
            qte.save()
            yep.done=True
            yep.save()
    context = {
        'data': pending
    }
    return render(request,'pending.html',context)

@login_required
def users(request):
    session = Profile.objects.filter(user=request.user.username)
    return render(request,'jump.html',{'sessions':session})

@login_required
def temp(request):
    if request.session['profile']==None:
        return redirect(users)
    data = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
    if data.instagram:
        isoc=Insta_data.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
        postno=isoc.post
        followers=isoc.followers
        op = Insta.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
        username = op.username
        password = op.password
        threading.Thread(target=Int.insta_data, args=(request.user.username,username,password,request.session['profile'])).start()
        #multiprocessing.Process(target=Int.insta_data, args=(request.user.username,username,password,request.session['profile'])).start()


    else:
        postno=0
        followers=0

    if data.facebook:
        ifac=Facebook.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
        token=ifac.token
        page_id=ifac.page_id
        try:
            apid = requests.get("https://graph.facebook.com/"+page_id+"?access_token="+token+"&fields=fan_count,published_posts.limit(1).summary(total_count).since(1)")
            fan_count=apid.json()['fan_count']
            face_post=apid.json()['published_posts']['summary']['total_count']
        except:
            fan_count=0
            face_post=0
        
    else:
        facebook = 0
        fan_count=0
        face_post=0

    if data.twitter:
        itwit=Twitter.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
        consumer_key = itwit.consumer_key
        consumer_secret = itwit.consumer_secret
        access_token = itwit.access_token
        access_token_secret =itwit.access_token_secret

        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # authentication of access token and secret
        try:
            auth.set_access_token(access_token, access_token_secret)
            apix = tweepy.API(auth)
            userd = apix.get_user(itwit.username)
            tfollow=userd.followers_count
            tcount=userd.statuses_count
        except:
            tfollow=0
            tcount=0


    else:
        tfollow=0
        tcount=0

    session=Profile.objects.filter(user=request.user.username)

    context={'session':request.session['profile'],'tfollow':tfollow,'tcount':tcount,'ipost':postno,'ifollow':followers,'face_post':face_post,'face_likes':fan_count}
    return render(request,'reset.html',context)

@login_required
def set_pro(request):
    if request.method=='POST':
        form=SetProfie(request.POST)
        if form.is_valid():
            form.instance.user=request.user.username
            r=Profile.objects.filter(Q(name=request.POST.get('name')) & Q(user=request.user.username))
            if r.count()>0 or request.POST.get('name')=='None':
                return render(request, 'set_profile.html', {'form': form,'error':1})
            form.save()
            get=Pro.objects.get(user=request.user)
            get.profile=get.profile+1
            get.save()
            return redirect('users')
        else:
            return render(request, 'set_profile.html', {'form': form})
    return render(request,'set_profile.html',{'form':SetProfie()})


@login_required
def cool(request,name):
    r=Profile.objects.filter(Q(name=name) & Q(user=request.user.username))
    if r.count()>0:
        request.session['profile']=name
        return redirect('aws')
    else:
        return redirect('users')


@login_required
def update(request,name):
    if request.method=='POST':
        if name=='instagram':
            form=Finsta(request.POST)
            if form.is_valid():
                ipp=Insta.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
                ipp.username=request.POST.get('username')
                ipp.password=request.POST.get('password')
                ipp.save()

        elif name=='facebook':
            form=Face(request.POST)
            if form.is_valid():
                ipp = Facebook.objects.get(Q(user=request.user) & Q(profile=request.session['profile']))
                ipp.token = request.POST.get('token')
                ipp.page_id = request.POST.get('page_id')
                ipp.save()

    rec = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
    if name=='instagram':
        if not rec.instagram:
            return redirect('aws')
        else:
            ipp=Insta.objects.get(Q(user=request.user)& Q(profile=request.session['profile']))
            return render(request,'setup.html',{'isu':1,'name':name,'form':Finsta(instance=ipp)})
    elif name=='facebook':

        if not rec.facebook:
            return redirect('aws')
        else:
            ipp = Facebook.objects.get(Q(user=request.user)& Q(profile=request.session['profile']))
            return render(request,'setup.html',{'isu':1,'name':name,'form':Face(instance=ipp)})
    elif name=='twitter':
        if not rec.twitter:
            return redirect('aws')
        else:
            ipp = Twitter.objects.get(Q(user=request.user)& Q(profile=request.session['profile']))
            return render(request,'setup.html',{'social':'twitter','isu':1,'name':name,'form':Twit(instance=ipp)})
    elif name=='linkd':
        if not rec.linkd:
            return redirect('aws')
        else:
            ipp = LinkD.objects.get(Q(user=request.user)& Q(profile=request.session['profile']))
            return render(request,'setup.html',{'social':'linkd','isu':1,'name':name,'form':Twit(instance=ipp)})

def delete(request,name):
    if name == 'instagram':
        Insta.objects.get(Q(user=request.user) & Q(profile=request.session['profile'])).delete()
        Insta_data.objects.get(Q(user=request.user) & Q(profile=request.session['profile'])).delete()
        make=Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        make.instagram=False
        make.save()
    if name == 'facebook':
        Facebook.objects.get(Q(user=request.user) & Q(profile=request.session['profile'])).delete()
        make = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        make.facebook = False
        make.save()

    if name == 'twitter':
        Twitter.objects.get(Q(user=request.user) & Q(profile=request.session['profile'])).delete()
        make = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        make.twitter = False
        make.save()

    if name == 'linkd':
        LinkD.objects.get(Q(user=request.user) & Q(profile=request.session['profile'])).delete()
        make = Profile.objects.get(Q(user=request.user) & Q(name=request.session['profile']))
        make.linkd = False
        make.save()

    return redirect('aws')

@login_required
def post_history(request):
    up=Iupload.objects.filter(Q(users=request.user) & Q(done=1) & Q(profile=request.session['profile']))
    return render(request,'post_history.html',{'up':up})

def download_image(request, id):
    img = Iupload.objects.get(id=id)
    filename='images.png'
    if img.users==request.user.username:
        image_buffer = open('media/'+str(img.file), "rb").read()
        content_type = magic.from_buffer(image_buffer, mime=True)
        response = HttpResponse(image_buffer, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response

def history(request):

    up = Save.objects.filter(Q(user=request.user) & Q(profile=request.session['profile']))
    for i in up:
        gg=Iupload.objects.get(id=i.fid)
        i.ndate=gg.date
        i.instagram=gg.instagram
        i.facebook=gg.facebook
        i.twitter=gg.twitter
        i.linkd = gg.linkd
        i.done=gg.done
        i.caption=gg.caption
    print(up)
    return render(request,'history.html',{'up':up})

def deletep(request,id):
    dd=Save.objects.get(id=id)
    if dd.done==0:
        nid=dd.fid
        dd.delete()
        Iupload.objects.get(id=nid).delete()
        return redirect('history')
    else:
        return Http404

@login_required
def fb_login(request):
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    show_user_url = 'https://api.twitter.com/1.1/users/show.json'
    consumer = oauth.Consumer(
            'C9rcyMD5v6K9W0ZBcGFoGaaTW', 'Yu7Kz3bAiItGP6H0SpU6CLSD5b1NnKqYHpiyLq1sbwAHTHx2ES')
    client = oauth.Client(consumer)
    resp, content = client.request("https://api.twitter.com/oauth/request_token", "POST", body=urllib.parse.urlencode({
            "oauth_callback": "http://django-env.eba-834pk48p.ap-south-1.elasticbeanstalk.com/fb/"}))
    request_token = dict(urllib.parse.parse_qsl(content))
    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')
    oauth_callback_confirmed = request_token[b'oauth_callback_confirmed'].decode('utf-8')
    return redirect("https://api.twitter.com/oauth/authorize?oauth_token="+oauth_token)

@login_required
def t_login(request):
    oauth_token=request.GET.get('oauth_token')
    oauth_verifier=request.GET.get('oauth_verifier')
    consumer = oauth.Consumer(
        'C9rcyMD5v6K9W0ZBcGFoGaaTW', 'Yu7Kz3bAiItGP6H0SpU6CLSD5b1NnKqYHpiyLq1sbwAHTHx2ES')
    client = oauth.Client(consumer)
    resp, content = client.request("https://api.twitter.com/oauth/access_token", "POST", body=urllib.parse.urlencode({
        'oauth_consumer_key': 'C9rcyMD5v6K9W0ZBcGFoGaaTW','oauth_token':oauth_token,'oauth_verifier':oauth_verifier}))

    access_token = dict(urllib.parse.parse_qsl(content))
    real_oauth_token = access_token[b'oauth_token'].decode('utf-8')
    real_oauth_token_secret = access_token[b'oauth_token_secret'].decode('utf-8')
    username = access_token[b'screen_name'].decode('utf-8')
    mon=Profile.objects.get(Q(name=request.session['profile']) & Q(user=request.user.username))
    if mon.twitter:
        get=Twitter.objects.get(Q(profile=request.session['profile']) & Q(user=request.user.username))
        get.access_token=real_oauth_token
        get.access_token_secret=real_oauth_token_secret
        get.username=username
        get.save()
    else:
        Twitter.objects.create(user=request.user.username,profile=request.session['profile'],username=username,access_token=real_oauth_token,access_token_secret=real_oauth_token_secret)
        mon.twitter=True
        mon.save()
    return redirect('aws')

def ggp(request):
    return render(request,'fb-login.html',{})

@login_required
def linkd(request):

    if request.GET.get('code'):
        code = request.GET.get('code')
        data = requests.get("https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code=" + str(
            code) + "&redirect_uri=http://django-env.eba-834pk48p.ap-south-1.elasticbeanstalk.com/linkd/&client_id=86uhfw4w57lw74&client_secret=VYbQfvNSmfOeTk4F")
        x = data.json()
        token=x['access_token']
        usd=requests.get("https://api.linkedin.com/v2/me/?oauth2_access_token="+token)
        y = usd.json()
        urn=y['id']
        mon = Profile.objects.get(Q(name=request.session['profile']) & Q(user=request.user.username))
        if mon.linkd:
            get = LinkD.objects.get(Q(profile=request.session['profile']) & Q(user=request.user.username))
            get.access_token = token
            get.urn = urn
            get.save()
        else:
            LinkD.objects.create(user=request.user.username, profile=request.session['profile'],
                                 access_token=token, urn=urn)
            mon.linkd = True
            mon.save()
        return redirect('aws')
    else:
        return redirect("https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=86uhfw4w57lw74&scope=r_liteprofile%20r_emailaddress%20w_member_social&redirect_uri=http://django-env.eba-834pk48p.ap-south-1.elasticbeanstalk.com/linkd/")



def abhiraj(request,to="jaswindersingh11061998@gmail.com"):
    import random

    list=['https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-37.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-1.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-4.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-23.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-17.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-41.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-40.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-40.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-39.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-32.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-24.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-20.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-27.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-22.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-18.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-15.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-16.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-12.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-10.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-10.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-8.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-7.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-6.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-11.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-9.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-2.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-25.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-30.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-31.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-42.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-42.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-35.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-34.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-33.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-38.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-36.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-29.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-28.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-26.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-21.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-19.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-14.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-13.png',
          'https://static.readerscave.com/2017/04/hindi-gaaliyan-in-english-3.png']

    length=len(list)
    p=random.randint(0, length-1)

    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    if request.method=='POST':
        place=request.POST.get('place')
        mess = request.POST.get('mess')
        subject = 'Abhiraj Ganda Banda Hai'
        html_message = render_to_string('abhiraj.html', {'form': 0, 'context': place,'mess':mess, 'image': list[p]})
        plain_message = strip_tags(html_message)
        from_email = 'MAP MEN <jaswindersingh11061998@yandex.com>'

        send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=False)

    subject = 'Abhiraj- Ganda Banda Hai'
    html_message = render_to_string('abhiraj.html', {'form':0,'context': 'GANDA BANDA','image':list[p]})
    plain_message = strip_tags(html_message)
    from_email = 'MEGA <shivsinghkhaira@gmail.com>'

    send_mail(subject, plain_message, from_email, [to],html_message=html_message,fail_silently=False)

    return render(request,'abhiraj.html',{'image':list[p],'form':1})