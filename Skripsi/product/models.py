from django.db import models
from embed_video.fields import EmbedVideoField

class Product (models.Model):
    productId = models.AutoField(primary_key=True,null=False)
    subCategoryId = models.BigIntegerField()
    brandId = models.BigIntegerField()
    productName = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    videoUrl = EmbedVideoField()
    minPrice = models.BigIntegerField() #lowest
    maxPrice = models.BigIntegerField() #highest
    dtm_crt = models.DateTimeField(null=False)
    productIMG = models.ImageField(null=False, blank=False,  default='none') #image belum ditambahin :(
