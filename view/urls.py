from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [

    path('',views.home,name='home'),
    path('iupload/',views.iupload,name='iupload'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutt,name='logout'),
    path('users/',views.users,name='users'),
    #path("login/", auth_views.LoginView.as_view(template_name="login.html",authentication_form=Customauth, redirect_authenticated_user=True), name="login"),
    path("login/", views.logind, name="login"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',

         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),

         name='password_reset_complete'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),name='password_reset_done'),

    path('setup/<name>',views.setup,name='setup'),
    path('update/<name>',views.update,name='update'),
    path('schedule/',views.sch,name='sch'),
    path('pending/',views.check,name='pending'),
    path('temp/',views.temp,name='temp'),
    path('delete/<name>',views.delete,name='delete'),
    path('post_history/',views.post_history,name='post_history'),
    path('sch_history/',views.history,name='history'),
    path('delete_p/<id>',views.deletep,name='delp'),
    path('download/<id>',views.download_image,name='download'),
    path('set_profile',views.set_pro,name="setp"),
    path('put_data/<name>',views.cool,name="cool"),
    path('aws/',views.temp,name='aws'),
    path('fbe/',views.fb_login,name="fbe"),
    path('fb/',views.t_login,name="fb"),
    path('twit/',views.ggp,name='ttw')
]

