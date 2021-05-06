from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('addProduct/',views.addProduct,name="addProduct"),

   #json
   path('addProduct/cat-json/',views.getJsonCategoryData,name="cat-json"),
   path('addProduct/subCat-json/<str:cat>',views.getJsonSubCategoryData,name="cat-json"),
]
