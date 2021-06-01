from django.contrib import admin

# Register your models here.
from .models import Review, HelpfulData, Report

admin.site.register(Review)
admin.site.register(HelpfulData)
admin.site.register(Report)
