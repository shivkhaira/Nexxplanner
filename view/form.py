from .models import Pro,Insta,Iupload,Facebook,Twitter,Save,Profile
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm

class Customauth(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'name':'username','placeholder':'Username','id':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input100', 'name':'password','placeholder':'Password','id':'password'}))

class Ureg(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150,widget=forms.TextInput(attrs={'class':'form__input','placeholder':'Username'}))
    email = forms.EmailField(label='Enter email',widget=forms.EmailInput(attrs={'class':'form__input','placeholder':'Email'}))
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class':'form__input','placeholder':'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form__input','placeholder':'Confirm Password'}))

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
    file=forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    caption=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control','rows':'8','placeholder':'Enter Your Caption'}))
    class Meta:
        model=Iupload
        fields=["file","caption"]

class Face(forms.ModelForm):
    token = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Token', 'autofocus': '1'}))
    page_id = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Page ID'}))

    class Meta:
        model=Facebook
        fields=["token","page_id"]

class Twit(forms.ModelForm):
    consumer_key = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Consumer Key', 'autofocus': '1'}))
    consumer_secret = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Consumer Scret'}))
    access_token = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Access Token', 'autofocus': '1'}))
    access_token_secret = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Access Token Secret'}))
    username = forms.CharField(max_length=100,
                                          widget=forms.TextInput(
                                              attrs={'class': 'form-control', 'placeholder': 'Twitter Username'}))

    class Meta:
        model=Twitter
        fields=['consumer_key','consumer_secret','access_token','access_token_secret','username']

    def __init__(self, *args, **kwargs):
        super(Twit, self).__init__(*args, **kwargs)
        self.fields['consumer_key'].label = "Consumer Key"
        self.fields['consumer_secret'].label = "Consumer Secret"
        self.fields['access_token'].label = "Access Token"
        self.fields['access_token_secret'].label = "Access Token Secret"
        self.fields['username'].label = "Twitter Username"

class Schedule(forms.ModelForm):
    sdate=forms.DateTimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    stime=forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control','type':'time'}))
    class Meta:
        model=Save
        fields=['sdate','stime']

    def __init__(self, *args, **kwargs):
        super(Schedule, self).__init__(*args, **kwargs)
        self.fields['sdate'].label = "Schedule Date"
        self.fields['stime'].label = "Schedule Time"

class ResetP(PasswordResetForm):
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'InputStyle','autocomplete':'new_password','required':'1'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'InputStyle','autocomplete':'new_password','required':'1'}))


class SetProfie(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name','email']

