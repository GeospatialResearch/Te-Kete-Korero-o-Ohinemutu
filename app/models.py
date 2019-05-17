from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
import uuid

# Create your models here.
class Dataset(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    name = models.CharField(max_length=200)


class PolygonEntity(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    geom = models.MultiPolygonField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    properties = JSONField(default=None, blank=True, null=True)
