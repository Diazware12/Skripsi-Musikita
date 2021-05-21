from django.db import models
from embed_video.fields import EmbedVideoField
from Skripsi import settings

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
    brandURL = models.URLField(max_length=200)
    description = models.CharField(max_length = 255)
    brandEmail = models.CharField(max_length=60,default='')
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=15)

class Product (models.Model):
    productId = models.AutoField(primary_key=True,null=False)
    categoryId = models.ForeignKey(Category,on_delete=models.CASCADE)
    subCategoryId = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brandId = models.ForeignKey(Brand,on_delete=models.CASCADE)
    productName = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    videoUrl = EmbedVideoField()
    minPrice = models.BigIntegerField() #lowest
    maxPrice = models.BigIntegerField() #highest
    dtm_crt = models.DateTimeField(null=False)
    productIMG = models.ImageField(upload_to=settings.MEDIA_ROOT+'/product',null=False, blank=False, default='none', max_length=255)
    visitCount = models.BigIntegerField(null=False,default=0)
    







