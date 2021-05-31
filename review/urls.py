from django.urls import path
from . import views

urlpatterns = [
   path('',views.reviewProduct,name="reviewProduct"),
   path('report/<user>',views.reportReview,name="reportReview"),
   path('<feedback>/<user>/',views.feedback,name="feedback")
]
