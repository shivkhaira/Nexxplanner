from .models import Pro,Insta,Iupload,Facebook,Twitter,Save
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings


class Ureg(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(Ureg, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].widget.attrs.update({'placeholder': ('Repeat password')})
        self.fields['password2'].widget.attrs.update({'class': ('form-control')})
        self.fields['password1'].widget.attrs.update({'class': ('form-control')})
        self.fields['password1'].widget.attrs.update({'placeholder': ('Password')})
        self.fields['username'].widget.attrs.update({'placeholder': ('Username')})
        self.fields['username'].widget.attrs.update({'class': ('form-control')})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.fields['email'].widget.attrs.update({'placeholder': ('Email')})
        self.fields['email'].widget.attrs.update({'class': ('form-control')})
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class Finsta(forms.ModelForm):

    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','autofocus':'1'}))
    password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model=Insta
        fields=['username','password']

class Uinsta(forms.ModelForm):

    class Meta:
        model=Iupload
        fields=["file","caption"]

class Face(forms.ModelForm):
    class Meta:
        model=Facebook
        fields=["token"]

class Twit(forms.ModelForm):
    class Meta:
        model=Twitter
        fields=['consumer_key','consumer_secret','access_token','access_token_secret']

    def __init__(self, *args, **kwargs):
        super(Twit, self).__init__(*args, **kwargs)
        self.fields['consumer_key'].label = "Consumer Key"
        self.fields['consumer_secret'].label = "Consumer Secret"
        self.fields['access_token'].label = "Access Token"
        self.fields['access_token_secret'].label = "Access Token Secret"

class Schedule(forms.ModelForm):
    sdate=forms.DateTimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    stime=forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control','type':'time'}))
    class Meta:
        model=Save
        fields=['sdate','stime']
