from django.conf.urls import url
from django.contrib import admin
from .views import registerMember,registerMusicStore
from django.urls import path
from . import views

urlpatterns = [
   path('regularUser/',views.registerMember,name="regularUser"),
   path('musicStore/',views.registerMusicStore,name="musicStore"),
   path('admin/<code>',views.registerAdmin,name="registerAdmin"),
   path('userApproveList/',views.musicStorePendingList,name="userApproveList"),
   path('userApproveList/<auth_token>',views.musicStoreApproval,name="userApproval"),
   path('userApproveList/<auth_token>/approveStatus',views.approve,name="approve"),
   path('userApproveList/<auth_token>/rejectionStatus/<context>',views.reject,name="reject"),
]
