from django.urls import path
from . import views

urlpatterns = [
   path('',views.reportList,name="reportList"),
   path('<user_select>/<brand>/<productName>',views.reportListView,name="reportListView"),
   path('<user_select>/<brand>/<productName>/approve',views.approveReport,name="approveReport"),
   path('<user_select>/<brand>/<productName>/reject',views.rejectReport,name="rejectReport"),
   # path('<user_select>/<brand>/<productName>/reject',views.reportListView,name="reportListView"),
]
