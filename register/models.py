from django.db import models

class User (models.Model):
    userID = models.AutoField(primary_key=True,null=False)
    userName = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    roleId = models.CharField(max_length=10)
    description = models.CharField(blank=True,max_length=255)
    status = models.CharField(max_length=15)
    dtm_crt = models.DateTimeField(null=False)
    auth_token = models.CharField(max_length=100,null=True) #
    verified_at = models.DateTimeField(null=True) #


class MusicStoreData (models.Model): #ganti nama
    musicStoreDataID = models.AutoField(primary_key=True,null=False)
    userID = models.BigIntegerField()
    address = models.CharField(blank=False,max_length=255)
    contact = models.CharField(null=False,max_length=16,default='') #
    musicStorePicture = models.ImageField(null=False, blank=False) #harus install pillow "python -m pip install Pillow"
