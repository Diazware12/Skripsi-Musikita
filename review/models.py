from django.db import models
from register.models import User
from product.models import Product
from datetime import datetime

class Review (models.Model):
    reviewId = models.AutoField(primary_key=True,null=False)
    productId = models.ForeignKey(Product,on_delete=models.CASCADE) 
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    dtm_crt = models.DateTimeField(null=False)
    title = models.CharField(blank=False,max_length=40)
    description = models.TextField()
    rating = models.IntegerField()
    helpful = models.BigIntegerField(default=0)
    notHelpful = models.BigIntegerField(default=0)

class HelpfulData (models.Model):
    helpfulDataId = models.AutoField(primary_key=True,null=False)
    reviewId = models.ForeignKey(Review,on_delete=models.CASCADE, default=1)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)

class Report (models.Model):
    reportId = models.AutoField(primary_key=True,null=False)
    reviewId = models.ForeignKey(Review,on_delete=models.CASCADE)
    userID = models.ForeignKey(User,on_delete=models.CASCADE) 
    reason = models.CharField(max_length=50)
