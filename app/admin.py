from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.gis.admin import GeoModelAdmin
from .models import Dataset, Story, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation

# Register your models here.

# admin.site.register(Dataset)

@register(Dataset)
class DatasetAdmin(ModelAdmin):
    list_display = ['name']


@register(Story)
class StoryAdmin(ModelAdmin):
    list_display = ['title']


@register(StoryBodyElement)
class StoryBodyElementAdmin(ModelAdmin):
    list_display = ['id', 'element_type']


@register(StoryGeomAttrib)
class StoryGeomAttribAdmin(GeoModelAdmin):
    list_display = ['name']


@register(StoryGeomAttribMedia)
class StoryGeomAttribMediaAdmin(ModelAdmin):
    list_display = ['id']


@register(MediaFile)
class MediaFileAdmin(ModelAdmin):
    list_display = ['file']


@register(WebsiteTranslation)
class WebsiteTranslationAdmin(ModelAdmin):
    list_display = ['field_name', 'eng', 'mao']
    readonly_fields = ["field_name"]

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
