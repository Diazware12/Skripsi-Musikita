from django.db import models
from register.models import User
from product.models import Product

class Review (models.Model):
    reviewId = models.AutoField(primary_key=True,null=False)
    productId = models.ForeignKey(Product,on_delete=models.CASCADE) 
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    dtm_crt = models.DateTimeField(null=False)
    title = models.CharField(blank=False,max_length=40)
    description = models.CharField(blank=False,max_length=255)
    rating = models.IntegerField()

class Report (models.Model):
    reportId = models.AutoField(primary_key=True,null=False)
    reviewId = models.ForeignKey(Review,on_delete=models.CASCADE) 
    reason = models.CharField(blank=False,max_length=255)
