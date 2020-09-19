from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .form import Ureg,Register,Finsta,Uinsta
from django.contrib import messages
from .autobot import Int
from .models import Insta,Iupload
import threading
import multiprocessing


from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.


def home(request):
    if request.method=='POST':
        form=Finsta(request.POST)
        if form.is_valid():
            form.save()

            return render(request,'index.html',{'form':Finsta(),'register':1})
    return render(request,'index.html',{'form':Finsta(),'active':'home'})

def json(request):
    pass

def iupload(request):
    if request.method=='POST':
        form=Uinsta(request.POST,request.FILES)
        if form.is_valid():
            data=form.save()
            pic=Iupload.objects.get(id=data.id)
            p = Insta.objects.get(id=1)
            img = str(pic.file)
            multiprocessing.Process(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            #threading.Thread(target=Int.up, args=(p.username,p.password,'media/'+img,data.caption)).start()
            return render(request, 'upload.html', {'form': Uinsta()})
        else:
            return redirect('home')

    return render(request,'upload.html',{'form':Uinsta()})

def hello(request):
   res = send_mail("hello paul", "view page", "shivsinghkhaira@gmail.com", ['shivsinghkhaira@gmail.com'])
   return HttpResponse('%s'%res)