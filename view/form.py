from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Pro,Insta,Iupload

class Ureg(UserCreationForm):

    class Meta:
        model=User
        fields=["username","password1","password2"]

    def __init__(self,*args,**kwargs):
        super(Ureg,self).__init__(*args,**kwargs)
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

class Register(forms.ModelForm):
    email = forms.EmailField(max_length=40,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email','autofocus':'1'}))
    class Meta:
        model=Pro
        fields=["email"]

    def __init__(self,*args,**kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.fields['email'].label="Email"

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

