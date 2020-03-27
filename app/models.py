from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
import uuid
from model_utils import Choices
from rest_framework.exceptions import ValidationError
from django.db.models import Q

# QuerySets
class StoryQuerySet(models.QuerySet):

    def for_user(self, user):
        # Not logged in? Only public data or data created by admin
        if not user.is_authenticated:
            return self.filter(Q(owner__is_superuser=True))
        # Super user? All the data!
        if user.is_superuser:
            return self.all()
        else:
            stories = [co_author.story.id for co_author in CoAuthor.objects.filter(co_author=user)]
            return self.filter(Q(owner=user)) | self.filter(Q(owner__is_superuser=True)) | self.filter(id__in=stories)

class StoryBodyElementQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Only public data or data created by admin
        if not user.is_authenticated:
            return self.filter(Q(story__owner__is_superuser=True)) # those stories the admin is the owner
        # Super user? All the data!
        if user.is_superuser:
            return self.all()
        else:
            stories = [co_author.story.id for co_author in CoAuthor.objects.filter(co_author=user)]
            return self.filter(Q(story__owner=user)) | self.filter(Q(story__owner__is_superuser=True)) | self.filter(story__id__in=stories)


class DatasetQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Only public data or data created by admin
        if not user.is_authenticated:
            return self.filter(Q(uploaded_by__is_superuser=True)) # those datasets uploaded by the admin
        # Super user? All the data!
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(Q(uploaded_by=user)) | self.filter(Q(uploaded_by__is_superuser=True)) | self.filter(Q(shared_with__contains=[user.id]))


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
    uploaded_by = models.ForeignKey('auth.User', related_name='datasets', on_delete=models.CASCADE)
    shared_with = ArrayField(models.IntegerField(), default=None, blank=True, null=True)
    style = JSONField(default=None, blank=True, null=True)
    objects = DatasetQuerySet.as_manager()


class StoryType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=200,blank=True, null=True)


class Atua(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Story(models.Model):
    STATUS = Choices(
        ('DRAFT', 'DRAFT'),
        ('SUBMITTED', 'SUBMITTED'),
        ('ACCEPTED', 'ACCEPTED'),
        ('PUBLISHED', 'PUBLISHED')
    )

    DATE_TYPE = Choices(
        ('PRECISE_DATE', 'PRECISE DATE'),
        ('DATE_RANGE', 'DATE RANGE')
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, primary_key=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = JSONField(default=None, blank=True, null=True)
    summary = JSONField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, default=STATUS.DRAFT, null=False, choices=STATUS)
    approx_time = JSONField(default=None, blank=True, null=True)
    atua =  models.ManyToManyField("Atua")
    story_type = models.ForeignKey(StoryType, blank=True, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='stories', on_delete=models.CASCADE)
    being_edited_by = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE)
    objects = StoryQuerySet.as_manager()

class CoAuthor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    story = models.ForeignKey(Story,related_name='coauthers', on_delete=models.CASCADE)
    co_author = models.ForeignKey('auth.User', related_name='coauthors', on_delete=models.CASCADE)


class MediaFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name


class StoryGeomAttrib(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    name = JSONField(default=None, blank=True, null=True)
    description = JSONField(default=None, blank=True, null=True)
    style = JSONField(default=None, blank=True, null=True)
    geometry = models.GeometryField()


class StoryGeomAttribMedia(models.Model):
    MEDIA_TYPES = Choices(
        ('IMG', 'IMG'),
        ('AUDIO', 'AUDIO'),
        ('VIDEO', 'VIDEO')
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    geom_attr = models.ForeignKey(StoryGeomAttrib, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=20, default=MEDIA_TYPES.IMG, null=False, choices=MEDIA_TYPES)
    mediafile_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    mediafile = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    media_description = JSONField(default=None, blank=True, null=True)


class ContentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)


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
    text = JSONField(default=None, blank=True, null=True)
    mediafile_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    mediafile = models.ForeignKey(MediaFile, on_delete=models.CASCADE, blank=True, null=True)
    media_description = JSONField(default=None, blank=True, null=True)
    geom_attr = models.ForeignKey(StoryGeomAttrib, on_delete=models.CASCADE, blank=True, null=True)
    order_position = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType,blank=True, null=True,on_delete=models.CASCADE)

    objects = StoryBodyElementQuerySet.as_manager()


class WebsiteTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=300,unique=True)
    eng = models.CharField(max_length=300)
    mao = models.CharField(max_length=300)


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
