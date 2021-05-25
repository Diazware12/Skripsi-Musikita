from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('addProduct/',views.addProduct,name="addProduct"),
   path('category/<categoryName>/',views.viewProductByCategory,name="category"),
   path('<brand>/<productName>/',views.showProduct,name="showProduct"),
   path('<brand>/<productName>/review',include('review.urls')),

   #json
   path('addProduct/cat-json/',views.getJsonCategoryData,name="cat-json"),
   path('addProduct/subCat-json/<str:cat>',views.getJsonSubCategoryData,name="cat-json"),
]
