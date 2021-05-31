from django.urls import path
from . import views

urlpatterns = [
   path('<userName>',views.profilePage,name="profilePage"),
   path('<userName>/edit/profilePicture',views.editProfilePicture,name="editProfilePicture"),
   path('<userName>/edit/userData',views.editUserData,name="editUserData"),
]