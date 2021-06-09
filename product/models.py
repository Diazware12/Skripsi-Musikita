from django.db import models
from embed_video.fields import EmbedVideoField
from Skripsi import settings
from datetime import datetime

class Category (models.Model):
    categoryId = models.AutoField(primary_key=True,null=False)
    categoryName = models.CharField(max_length = 50)

class SubCategory (models.Model):
    subCategoryId = models.AutoField(primary_key=True,null=False)
    categoryId = models.ForeignKey(Category,on_delete=models.CASCADE)
    subCategoryName = models.CharField(max_length = 50)

class Brand (models.Model):
    brandId = models.AutoField(primary_key=True,null=False)
    brandName = models.CharField(max_length = 50)
    brandURL = models.URLField(max_length=200,null=True)
    description = models.CharField(max_length = 255,null=True)
    brandEmail = models.CharField(max_length=60,default='',null=True)
    status = models.CharField(max_length=15,blank=False,null=False,default='No_User')
    auth_token = models.CharField(max_length=100,null=True)

class Product (models.Model):
    productId = models.AutoField(primary_key=True,null=False)
    categoryId = models.ForeignKey(Category,on_delete=models.CASCADE)
    subCategoryId = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brandId = models.ForeignKey(Brand,on_delete=models.CASCADE)
    productName = models.CharField(max_length = 50)
    description = models.TextField()
    videoUrl = EmbedVideoField()
    dtm_crt = models.DateTimeField(null=False)
    dtm_upd = models.DateTimeField(default=datetime.now,null=False)
    productIMG = models.ImageField(upload_to=settings.MEDIA_ROOT+'/product',null=False, blank=False, default='none', max_length=255)
    visitCount = models.BigIntegerField(null=False,default=0)
    avgScore = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    editorChoice = models.BooleanField(default=False)
    







