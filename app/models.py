from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from model_utils import Choices


# Create your models here.
class Dataset(models.Model):
    POINT = 0
    LINE = 1
    POLYGON = 2
    GEOMTYPES = Choices(
        (POINT, 'POINT'),
        (LINE, 'LINE'),
        (POLYGON, 'POLYGON')
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


class PolygonEntity(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.MultiPolygonField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    attributes = JSONField(default=None, blank=True, null=True)

    class Meta:
        db_table = "app_polygon_entity"


class LineEntity(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.MultiLineStringField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    attributes = JSONField(default=None, blank=True, null=True)

    class Meta:
        db_table = "app_line_entity"


class PointEntity(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.MultiPointField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    attributes = JSONField(default=None, blank=True, null=True)

    class Meta:
        db_table = "app_point_entity"
