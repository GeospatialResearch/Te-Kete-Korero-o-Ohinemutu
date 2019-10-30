from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from model_utils import Choices
from rest_framework.exceptions import ValidationError
from ckeditor.fields import RichTextField


# Create your models here.
class Dataset(models.Model):
    POINT = 0
    LINE = 1
    POLYGON = 2
    RASTER = 3
    GEOMTYPES = Choices(
        (POINT, 'POINT'),
        (LINE, 'LINE'),
        (POLYGON, 'POLYGON'),
        (RASTER, 'RASTER')
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    name = models.CharField(max_length=200)
    geomtype = models.IntegerField(null=False,
                                default=POINT,
                                choices=GEOMTYPES)
    assigned_name = models.CharField(max_length=200, default=None, blank=True, null=True)


class Story(models.Model):
    STATUS = Choices(
        ('DRAFT', 'DRAFT'),
        ('SUBMITTED', 'SUBMITTED'),
        ('ACCEPTED', 'ACCEPTED'),
        ('PUBLISHED', 'PUBLISHED')
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, default=STATUS.DRAFT, null=False, choices=STATUS)


class MediaFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name


class StoryGeometry(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    geom = models.GeometryField()


class StoryGeomAttrib(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    style = JSONField(default=None, blank=True, null=True)
    geometry = models.ForeignKey(StoryGeometry, on_delete=models.CASCADE)


class StoryBodyElement(models.Model):
    ELEMENT_TYPES = Choices(
        ('TEXT', 'TEXT'),
        ('IMG', 'IMG'),
        ('AUDIO', 'AUDIO'),
        ('VIDEO', 'VIDEO'),
        ('GEOM', 'GEOM')
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    element_type = models.CharField(max_length=20, default=ELEMENT_TYPES.TEXT, null=False, choices=ELEMENT_TYPES)
    text = RichTextField(default=None, blank=True, null=True)
    mediafile_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    mediafile = models.ForeignKey(MediaFile, on_delete=models.CASCADE, blank=True, null=True)
    media_description = models.TextField(max_length=400, default=None, blank=True, null=True)
    geom_attr = models.ForeignKey(StoryGeomAttrib, on_delete=models.CASCADE, blank=True, null=True)
    order_position = models.IntegerField(blank=True, null=True)
