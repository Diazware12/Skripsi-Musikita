from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('brandcontrol',views.brandControl,name="brandControl"),
    path('brandcontrol/add',views.addBrand,name="addBrand"),
    path('brandcontrol/invite',views.inviteBrand,name="inviteBrand"),
    path('registerBrand/<auth_token>',views.registerBrand,name="registerBrand"),
    path('<brandName>/<sort>',views.brandPage,name="brandPage")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)