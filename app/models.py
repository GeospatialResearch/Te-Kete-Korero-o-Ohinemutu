from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from model_utils import Choices


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
