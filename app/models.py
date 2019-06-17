from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from model_utils import Choices

GEOMTYPES = Choices(
    ('POINT', '1'),
    ('LINE', '2'),
    ('POLYGON', '3')
)


# Create your models here.
class Dataset(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    name = models.CharField(max_length=200)
    geomtype = models.CharField(max_length=10,
                                null=False,
                                default=GEOMTYPES.POINT,
                                choices=GEOMTYPES)


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
