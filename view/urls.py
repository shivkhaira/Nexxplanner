from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',views.home,name='home'),
    path('iupload/',views.iupload,name='iupload'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutt,name='logout'),
    path('users/',views.users,name='users'),
    path("login/", auth_views.LoginView.as_view(template_name="index.html"), name="login"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('setup/<name>',views.setup,name='setup'),
    path('schedule/',views.sch,name='sch'),
    path('pending/',views.check,name='pending')
]