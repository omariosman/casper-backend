from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views
 
from .models import *
 
urlpatterns = [
    path('send_address/', views.send_address, name="send_address"),

]