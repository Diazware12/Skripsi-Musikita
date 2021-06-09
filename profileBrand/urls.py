from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('brandcontrol',views.brandControl,name="brandcontrol"),
    path('brandcontrol/add',views.addBrand,name="addBrand"),
    path('brandcontrol/invite',views.inviteBrand,name="inviteBrand"),
    path('brandcontrol/<brand>/reset',views.resetInvitation,name="resetInvitation"),
    path('brandcontrol/<brand>/delete',views.deleteBrand,name="deleteBrand"),
    path('brandcontrol/<brand>/deleteReason',views.deleteBrandWithReason,name="deleteBrandWithReason"),
    path('registerBrand/<auth_token>',views.registerBrand,name="registerBrand"),

    path('<brandName>/<sort>',views.brandPage,name="brandPage"),
    path('<brandName>/<context>/edit',views.brandEdit,name="brandEdit")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)