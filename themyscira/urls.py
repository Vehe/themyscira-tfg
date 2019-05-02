from django.urls import path
from . import views

app_name = 'themyscira'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('foro/', views.forum, name='foro'),
    path('foro/getnotify/', views.getnotify, name='getnotify'),
    path('foro/addresponse/', views.addresponse, name='addresponse'),
    path('foro/addquestion/', views.addquestion, name='addquestion'),
]
