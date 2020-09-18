from django.urls import path
from . import views
urlpatterns = [

    path('',views.home,name='home'),
    path('iupload/',views.iupload,name='iupload'),
    path('hello/',views.hello,name='hello')
]