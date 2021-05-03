
from django.conf.urls import url
from django.contrib import admin
from .views import *

from . import views

urlpatterns = [
   url(r'^regularUser/',views.registerMember),
   url(r'^musicStore/',views.registerMusicStore)
]
