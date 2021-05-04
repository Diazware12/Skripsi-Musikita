from django.conf.urls import url
from django.contrib import admin
from .views import registerMember,registerMusicStore
from django.urls import path
from . import views

urlpatterns = [
   path('regularUser/',views.registerMember,name="regularUser"),
   path('musicStore/',views.registerMusicStore,name="musicStore")
   # url(r'^regularUser/',views.registerMember),
   # url(r'^musicStore/',views.registerMusicStore)
]
