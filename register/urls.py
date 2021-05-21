from django.conf.urls import url
from django.contrib import admin
from .views import registerMember,registerMusicStore
from django.urls import path
from . import views

urlpatterns = [
   path('regularUser/',views.registerMember,name="regularUser"),
   path('musicStore/',views.registerMusicStore,name="musicStore"),
   path('userApproveList/',views.musicStorePendingList,name="userApproveList"),
   path('userApproveList/<auth_token>',views.musicStoreApprove,name="userApproval")
   # url(r'^regularUser/',views.registerMember),
   # url(r'^musicStore/',views.registerMusicStore)
]
