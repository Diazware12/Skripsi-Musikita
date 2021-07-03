from django.db import models
from Skripsi import settings
from django.core.exceptions import ObjectDoesNotExist

class User (models.Model):
    userID = models.AutoField(primary_key=True,null=False)
    userName = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    roleId = models.CharField(max_length=10)
    description = models.TextField()
    status = models.CharField(max_length=15)
    dtm_crt = models.DateTimeField(null=False)
    auth_token = models.CharField(max_length=100,null=True) #
    verified_at = models.DateTimeField(null=True) #
    profilePicture = models.ImageField(upload_to=settings.MEDIA_ROOT+'/userProfiles', max_length=255, default='')

class MusicStoreData (models.Model): #ganti nama
    musicStoreDataID = models.AutoField(primary_key=True,null=False)
    userID = models.ForeignKey(User,on_delete=models.CASCADE) #
    address = models.TextField(blank=False)
    contact = models.CharField(null=False,max_length=16,default='') #
    musicStorePicture = models.ImageField(null=False, blank=False, upload_to=settings.MEDIA_ROOT+'/musicStorePictures', max_length=255)
    musicStorePicture2 = models.ImageField(null=False, blank=False, upload_to=settings.MEDIA_ROOT+'/musicStorePictures', max_length=255, default='')
    musicStorePicture3 = models.ImageField(null=False, blank=False, upload_to=settings.MEDIA_ROOT+'/musicStorePictures', max_length=255, default='')
