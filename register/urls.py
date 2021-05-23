from django.conf.urls import url
from django.contrib import admin
from .views import registerMember,registerMusicStore
from django.urls import path
from . import views

urlpatterns = [
   path('regularUser/',views.registerMember,name="regularUser"),
   path('musicStore/',views.registerMusicStore,name="musicStore"),
   path('userApproveList/',views.musicStorePendingList,name="userApproveList"),
   path('userApproveList/<auth_token>',views.musicStoreApproval,name="userApproval"),
   path('userApproveList/<auth_token>/approveStatus',views.approve,name="approve"),
   path('userApproveList/<auth_token>/rejectionStatus',views.reject,name="reject"),
   # path('userApproveList/<auth_token>/reject',views.musicStoreApproval,name="reject")
   # url(r'^regularUser/',views.registerMember),
   # url(r'^musicStore/',views.registerMusicStore)
]
