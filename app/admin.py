from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import Dataset

# Register your models here.

# admin.site.register(Dataset)

@register(Dataset)
class DatasetAdmin(ModelAdmin):
    list_display = ['name']
