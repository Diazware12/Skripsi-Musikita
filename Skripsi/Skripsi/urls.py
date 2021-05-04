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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.dashboard),
    url(r'^rating/',views.rating),
    url(r'^profile/',views.profile),
    url(r'^profileMusicStore/',views.profileMusicStore),
    url(r'^scoreRating/',views.scoreRating),
    url(r'^productList/',views.productList),
    url(r'^userApproveList/',views.userApproveList),
    # url(r'^register/',include('register.urls')),
    path('register/',include('register.urls'),name="register"),
    path('product/',include('product.urls'),name="product"),
    url(r'^success/',views.token),
    path('verify/<auth_token>',views.verifyEmail,name="verify"),
]
