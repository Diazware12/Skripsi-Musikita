from django.urls import path
from . import views

urlpatterns = [
   path('',views.reviewProduct,name="reviewProduct"),
   path('update/<action>/<user_select>',views.updateReview,name="updateReview"),
   path('delete/<action>/<user_select>',views.deleteReview,name="deleteReview"),
   path('report/<user>',views.reportReview,name="reportReview"),
   path('<feedback>/<user>/',views.feedback,name="feedback")
]
