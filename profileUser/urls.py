from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
   path('<userName>',views.profilePage,name="profilePage"),
   path('<userName>/edit/profilePicture',views.editProfilePicture,name="editProfilePicture"),
   path('<userName>/edit/userData',views.editUserData,name="editUserData"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)