"""Skripsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('',views.dashboard,name="dashboard"),
    path('logout/',views.user_logout,name="logoutUser"),
    path('profile/',include('profileUser.urls')),
    url(r'^productList/',views.productList),
    path('register/',include('register.urls'),name="register"),
    path('product/',include('product.urls'),name="product"),
    path('brand/',include('profileBrand.urls'),name="brand"),
    path('carousel/',include('carousel.urls'),name="carousel"),
    path('reportList/',include('report.urls'),name="report"),
    path('verify/<auth_token>',views.verifyEmail,name="verify"),
    path('forgot_Pass/<auth_token>',views.forgotPasswordForm,name="forgot_pass"),

    #quick qearch
    path('search/',views.search,name="search"),

    #advance search
    path('advancesearch/',include('advancesearch.urls'),name="aSearch")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
