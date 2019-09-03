from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.gis.admin import GeoModelAdmin
from .models import Dataset, Story, StoryGeomAttrib, StoryPointGeom, StoryLineGeom, StoryPolygonGeom

# Register your models here.

# admin.site.register(Dataset)

@register(Dataset)
class DatasetAdmin(ModelAdmin):
    list_display = ['name']
    

@register(Story)
class StoryAdmin(ModelAdmin):
    list_display = ['title']


@register(StoryGeomAttrib)
class StoryGeomAttribAdmin(ModelAdmin):
    list_display = ['name']


@register(StoryPointGeom)
class StoryPointGeomAdmin(GeoModelAdmin):
    list_display = ['id','geom']

    fieldsets = (
        (None, {'fields': []}),
        ('Geometry', {'fields': ['geom']})
    )

@register(StoryLineGeom)
class StoryLineGeomAdmin(GeoModelAdmin):
    list_display = ['geom']

    fieldsets = (
        (None, {'fields': []}),
        ('Geometry', {'fields': ['geom']})
    )

@register(StoryPolygonGeom)
class StoryPolygonGeomAdmin(GeoModelAdmin):
    list_display = ['geom']

    fieldsets = (
        (None, {'fields': []}),
        ('Geometry', {'fields': ['geom']})
    )
