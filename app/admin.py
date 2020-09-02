from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.gis.admin import GeoModelAdmin
from .models import Dataset, Story, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation, Atua, StoryType, ContentType, Comment, Profile, Sector, Nest, Publication
# TribalRegisterList

# Register your models here.

admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Publication)
# admin.site.register(TribalRegisterList)

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
    readonly_fields = ["field_name"] # since the variables in the website code depend on the field_name

    # disable add and delete records since the field_name must be used in the website code
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@register(Atua)
class AtuaAdmin(ModelAdmin):
    list_display = ['name']


@register(StoryType)
class StoryTypeAdmin(ModelAdmin):
    list_display = ['type']


@register(Sector)
class SectorAdmin(ModelAdmin):
    list_display = ['name']


@register(Nest)
class NestAdmin(ModelAdmin):
    list_display = ['name', 'get_kinshipsector_name']

    def get_kinshipsector_name(self, obj):
        return obj.kinship_sector.name
