from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.gis.admin import GeoModelAdmin
from .models import Dataset, Story, StoryGeometry, StoryGeomAttrib, StoryBodyElement, MediaFile

# StoryPointGeom, StoryLineGeom, StoryPolygonGeom,

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
class StoryGeomAttribAdmin(ModelAdmin):
    list_display = ['name']


@register(StoryGeometry)
class StoryGeometryAdmin(GeoModelAdmin):
    list_display = ['id','geom']

    fieldsets = (
        (None, {'fields': []}),
        ('Geometry', {'fields': ['geom']})
    )


# @register(StoryPointGeom)
# class StoryPointGeomAdmin(GeoModelAdmin):
#     list_display = ['id','geom']
#
#     fieldsets = (
#         (None, {'fields': []}),
#         ('Geometry', {'fields': ['geom']})
#     )
#
# @register(StoryLineGeom)
# class StoryLineGeomAdmin(GeoModelAdmin):
#     list_display = ['geom']
#
#     fieldsets = (
#         (None, {'fields': []}),
#         ('Geometry', {'fields': ['geom']})
#     )
#
# @register(StoryPolygonGeom)
# class StoryPolygonGeomAdmin(GeoModelAdmin):
#     list_display = ['geom']
#
#     fieldsets = (
#         (None, {'fields': []}),
#         ('Geometry', {'fields': ['geom']})
#     )

@register(MediaFile)
class MediaFileAdmin(ModelAdmin):
    list_display = ['file']
