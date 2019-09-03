from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from model_utils import Choices
from rest_framework.exceptions import ValidationError


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
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('ACCEPTED', 'Accepted'),
        ('PUBLISHED', 'Published')
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.TextField()
    summary = models.TextField()
    status = models.CharField(max_length=20, default=STATUS.DRAFT, null=False, choices=STATUS)


class StoryPointGeom(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.PointField()


class StoryLineGeom(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.LineStringField()


class StoryPolygonGeom(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.PolygonField()


class StoryGeomAttrib(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    name = models.CharField(max_length=30)
    description = models.TextField()
    style = JSONField(default=None, blank=True, null=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    point = models.ForeignKey(StoryPointGeom, on_delete=models.CASCADE, default=None, blank=True, null=True)
    line = models.ForeignKey(StoryLineGeom, on_delete=models.CASCADE, default=None, blank=True, null=True)
    polygon = models.ForeignKey(StoryPolygonGeom, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def clean(self):
        if not (self.point or self.line or self.polygon):
            raise ValidationError("You must specify one geometry.")
        if (self.point is not None and self.line is not None):
            raise ValidationError("Only one geometry should be specified.")
        elif (self.point is not None and self.polygon is not None):
            raise ValidationError("Only one geometry should be specified.")
        elif (self.line is not None and self.polygon is not None):
            raise ValidationError("Only one geometry should be specified.")
