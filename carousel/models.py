from Skripsi import settings
from django.db import models

class CarouselImage (models.Model):
    carouselId = models.AutoField(primary_key=True,null=False)
    carouselIMG = models.ImageField(upload_to=settings.MEDIA_ROOT+'/carousel',null=False, blank=False, default='none', max_length=255)
    status = models.BooleanField(default=False) #active/inactive
