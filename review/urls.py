from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('',views.reviewProduct,name="reviewProduct"),
   path('report/<user>',views.reportReview,name="reportReview"),
   path('<feedback>/<user>/',views.feedback,name="feedback")
]
