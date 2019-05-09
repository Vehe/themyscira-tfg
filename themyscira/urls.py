from django.urls import path
from . import views

app_name = 'themyscira'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('foro/', views.forum, name='foro'),
    path('requests/', views.requests, name='requests'),
    path('requests/addautor/', views.raddautor, name='raddautor'),
    #path('requests/', views.requests, name='requests'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/addautor', views.addautor, name='addautor'),
    path('contacto/addvideo', views.addvideo, name='addvideo'),
    path('foro/getnotify/', views.getnotify, name='getnotify'),
    path('foro/addresponse/', views.addresponse, name='addresponse'),
    path('foro/addquestion/', views.addquestion, name='addquestion'),
]
