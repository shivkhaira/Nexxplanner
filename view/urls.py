from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('edit_project/',views.edit_project,name='edit_project'),
    path('profile/',views.profile,name='profile'),
    path('edit_post/<id>',views.edit_post,name='edit_post'),
    path('view_image/<id>',views.view_image,name='view_image'),
    path('delete_profile/',views.delete_profile,name="delete_profile"),
    path('project/',views.project,name='project'),
    path('aws/',views.users,name='aws'),
    path('',views.home,name='home'),
    path('iupload/',views.iupload,name='iupload'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutt,name='logout'),
    path('users/',views.test,name='users'),
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

    path('setup/',views.setup,name='setup'),
    path('update/<name>',views.update,name='update'),
    path('schedule/',views.sch,name='sch'),
    path('pending/',views.check,name='pending'),
    path('temp/',views.temp,name='temp'),
    path('delete/<name>',views.delete,name='delete'),
    path('post_history/',views.post_history,name='post_history'),
    path('sch_history/',views.history,name='history'),
    path('delete_p/<id>',views.deletep,name='delp'),
    path('download/<id>',views.download_image,name='download'),
    path('set_profile/',views.set_pro,name="setp"),
    path('put_data/<name>',views.cool,name="cool"),
    path('fbe/',views.fb_login,name="fbe"),
    path('fb/',views.t_login,name="fb"),
    path('twit/',views.ggp,name='ttw'),
    path('linkd/',views.linkd,name='linkd'),
    path('abhiraj/<to>',views.abhiraj,name='abhi'),
    path('abhiraj/',views.abhiraj,name='abhi'),
    path('terms/',views.terms,name='terms'),
    path('privacy/',views.terms,name='privacy'),
    path('support/',views.support,name='support')
]


