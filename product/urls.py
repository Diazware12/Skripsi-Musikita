from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('addProduct/',views.addProduct,name="addProduct"),
      path('addProduct/cat-json/',views.getJsonCategoryData,name="cat-json"),
      path('addProduct/subCat-json/<str:cat>',views.getJsonSubCategoryData,name="cat-json"),

   path('addEditProduct/<context>/<brand>/<productName>',views.addEditProduct,name="editProduct"),
      path('addEditProduct/<context>/<brand>/<productName>/cat-json/',views.getJsonCategoryDataEdit,name="cat-json"),
      path('addEditProduct/<context>/<brand>/<productName>/subCat-json/<str:cat>',views.getJsonSubCategoryData,name="cat-json"),
   path('addEditProduct/<context>/<brand>/<productName>/editPicture',views.addEditPictureContext,name="editPicture"),
   path('addEditProduct/<context>/<brand>/<productName>/deleteProduct',views.deleteProduct,name="deleteProduct"),
   
   path('addProduct/<brand>/<productName>/addPicture',views.addEditPicture,name="addProductPicture"),
   path('editor/',views.editorChoice,name="editorchoice"),
   path('hotitems/',views.hotItems,name="hotitems"),
   path('category/<categoryName>/',views.viewProductByCategory,name="category"),
   path('category/<categoryName>/<subCategoryName>/',views.viewProductBySubCategory,name="subcategory"),
   path('<brand>/<productName>/',views.showProduct,name="showProduct"),
   path('<brand>/<productName>/review',include('review.urls')),
   path('<brand>/<productName>/<showMore>',views.showMoreReview,name="showMoreReview"),
   


]
