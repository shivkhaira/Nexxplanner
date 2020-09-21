from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .form import Finsta,Uinsta,Ureg,Face,Twit,Schedule
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .autobot import Int
from .models import Insta,Iupload,Pro,Facebook,Twitter,Save
from datetime import datetime
import multiprocessing
from django.http import Http404
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse
from datetime import date,datetime
import time
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('users')
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

@ login_required (login_url='/login/', redirect_field_name=None)
def logoutt(request):
        logout(request)
        return redirect("register")

def register(request):

    if request.method == 'POST':
        form = Ureg(request.POST)
        if form.is_valid():
            f=form.save()
            Pro.objects.create(user=f.username)
            messages.success(request, 'Account created successfully')
            return redirect('register')


    f = Ureg()
    return render(request, 'register.html', {'form': f})

@login_required
def iupload(request):

    if request.method=='POST':
        form=Uinsta(request.POST,request.FILES)
        if form.is_valid():
            insta = request.POST.get('instagram')
            face = request.POST.get('facebook')
            twit = request.POST.get('twitter')
            form.instance.users=request.user
            form.instance.done=True
            if insta:
                form.instance.instagram=True
            if face:
                form.instance.facebook=True
            if twit:
                form.instance.twitter=True
            data=form.save()
            pic=Iupload.objects.get(id=data.id)
            p = Insta.objects.get(user=request.user)
            img = str(pic.file)


            fb=Facebook.objects.get(user=request.user)
            token=fb.token

            tw=Twitter.objects.get(user=request.user)
            consumer_key=tw.consumer_key
            consumer_secret=tw.consumer_secret
            access_token=tw.access_token
            access_token_secret=tw.access_token_secret

            if face:
                multiprocessing.Process(target=Int.face,
                                        args=(token,'media/' + img, data.caption)).start()
            if twit:
                multiprocessing.Process(target=Int.twit, args=(consumer_key,consumer_secret,access_token,access_token_secret,'media/' + img, data.caption)).start()
            if insta:
                multiprocessing.Process(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            #threading.Thread(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            return redirect('iupload')
        else:
            return redirect('home')
    data=Pro.objects.get(user=request.user)
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
    all=instagram+facebook+twitter
    if all == 0:
        return redirect('users')

    return render(request,'upload.html',{'form':Uinsta(),'instagram':instagram,'facebook':facebook,'twitter':twitter,'all':all})

@login_required
def users(request):
    data=Pro.objects.get(user=request.user)
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

    all=instagram+facebook+twitter
    return render(request,'users.html',{'active':'users','instagram':instagram,'facebook':facebook,'twitter':twitter,'all':all})

@login_required()
def setup(request,name):
    if request.method=='POST':
        if name=='instagram':
            form=Finsta(request.POST)
            if form.is_valid():
                form.instance.user=request.user
                form.save()
                rec=Pro.objects.get(user=request.user)
                rec.instagram=True
                rec.save()
                return redirect('users')
        elif name=='facebook':
            form=Face(request.POST)
            if form.is_valid():
                form.instance.user=request.user
                form.save()
                rec=Pro.objects.get(user=request.user)
                rec.facebook=True
                rec.save()
                return redirect('users')
        elif name=='twitter':
            form=Twit(request.POST)
            if form.is_valid():
                form.instance.user=request.user
                form.save()
                rec=Pro.objects.get(user=request.user)
                rec.twitter=True
                rec.save()
                return redirect('users')
    if name=='instagram':
        rec = Pro.objects.get(user=request.user)
        if rec.instagram:
            return redirect('users')
        else:
            return render(request,'setup.html',{'name':name,'form':Finsta()})
    elif name=='facebook':
        rec = Pro.objects.get(user=request.user)
        if rec.facebook:
            return redirect('users')
        else:
            return render(request,'setup.html',{'name':name,'form':Face()})
    elif name=='twitter':
        rec = Pro.objects.get(user=request.user)
        if rec.twitter:
            return redirect('users')
        else:
            return render(request,'setup.html',{'name':name,'form':Twit()})


def sch(request):
    if request.method=='POST':
        form=Schedule(request.POST)
        uform=Uinsta(request.POST,request.FILES)
        if form.is_valid() and uform.is_valid():
            insta = request.POST.get('instagram')
            face = request.POST.get('facebook')
            twit = request.POST.get('twitter')
            uform.instance.users = request.user
            if insta:
                uform.instance.instagram = True
            if face:
                uform.instance.facebook = True
            if twit:
                uform.instance.twitter = True
            data=uform.save()
            form.instance.fid=data.id
            form.instance.user=request.user
            p=form.save()
            print(p.sdate)
        else:
            return Http404
    data = Pro.objects.get(user=request.user)
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
    return render(request,'schedule.html',{'form':Uinsta(),'form1':Schedule(),'instagram':instagram,'facebook':facebook,'twitter':twitter})

def check(request):

    curr = (datetime.now())
    pending = Save.objects.filter(done=False)
    for i in pending:
        dt = datetime.combine(i.sdate, i.stime)
        if curr >= dt:
            data = Iupload.objects.get(id=i.fid)
            if data.facebook:
                face = Facebook.objects.get(user=i.user)
                token = face.token
                multiprocessing.Process(target=Int.face,args=(token, 'media/' + str(data.file), data.caption)).start()
            if data.twitter:
                twit = Twitter.objects.get(user=i.user)
                consumer_key = twit.consumer_key
                consumer_secret = twit.consumer_secret
                access_token = twit.access_token
                access_token_secret = twit.access_token_secret
                multiprocessing.Process(target=Int.twit, args=(consumer_key, consumer_secret, access_token, access_token_secret, 'media/' + str(data.file),data.caption)).start()
            if data.instagram:
                insta = Insta.objects.get(user=i.user)
                username = insta.username
                password = insta.password
                multiprocessing.Process(target=Int.up, args=(username, password, 'media/' + str(data.file), data.caption)).start()
            yep=Save.objects.get(id=i.id)
            yep.done=True
            yep.save()
    context = {
        'data': pending
    }
    return render(request,'pending.html',context)