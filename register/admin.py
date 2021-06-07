from django.contrib import admin

# Register your models here.
from .models import User, MusicStoreData
admin.site.register(MusicStoreData)
admin.site.register(User)