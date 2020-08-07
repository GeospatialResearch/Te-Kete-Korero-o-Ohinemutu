from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
import uuid
from model_utils import Choices
from django.db.models import Q
from django.contrib.auth.models import User

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
            # stories that user is a kaitiaki
            stories_kaitiaki = [publication.story.id for publication in Publication.objects.filter(nest__kaitiaki__id=user.profile.id)]
            # stories that user is co-author
            stories_coauthor = [co_author.story.id for co_author in CoAuthor.objects.filter(co_author=user)]
            # stories published in nests that user belongs to
            stories_published_nest_member = [publication.story.id for publication in Publication.objects.filter(nest__members__id=user.profile.id, status='PUBLISHED')]
            # the above plus stories that user is owner and stories created by admin
            return self.filter(Q(owner=user)) | self.filter(Q(owner__is_superuser=True)) | self.filter(id__in=stories_coauthor) | self.filter(id__in=stories_kaitiaki) | self.filter(id__in=stories_published_nest_member)

class StoryBodyElementQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Only public data or data created by admin
        if not user.is_authenticated:
            return self.filter(Q(story__owner__is_superuser=True)) # those stories the admin is the owner
        # Super user? All the data!
        if user.is_superuser:
            return self.all()
        else:
            # stories that user is a kaitiaki
            stories_kaitiaki = [publication.story.id for publication in Publication.objects.filter(nest__kaitiaki__id=user.profile.id)]
            # stories that user is co-author
            stories_coauthor = [co_author.story.id for co_author in CoAuthor.objects.filter(co_author=user)]
            # stories published in nests that user belongs to
            stories_published_nest_member = [publication.story.id for publication in Publication.objects.filter(nest__members__id=user.profile.id, status='PUBLISHED')]
            # the above plus stories that user is owner and stories created by admin
            return self.filter(Q(story__owner=user)) | self.filter(Q(story__owner__is_superuser=True)) | self.filter(story__id__in=stories_coauthor) | self.filter(story__id__in=stories_kaitiaki) | self.filter(story__id__in=stories_published_nest_member)


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


class NestQuerySet(models.QuerySet):
    def for_user(self, user):
        whanausector = Sector.objects.get(name='Whānau')

        # Not logged in? Don't have access
        if not user.is_authenticated:
            return
        # Is superuser? Get all
        if user.is_superuser:
            return self.all()
        # Is staff? Gel all nests except whanau groups (users private)
        if user.is_staff:
            return self.filter(Q(members__id=user.profile.id) | ~Q(kinship_sector_id=whanausector.id)).distinct()
        # Regular user? Get only the nests the user is member
        else:
            # return self.filter(Q(members__id=user.profile.id)
            # to display all available nests for the normal user to view
            return self.all()


class WhanauGroupInvitationQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Don't have access
        if not user.is_authenticated:
            return
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(Q(nest__created_by=user)) | self.filter(Q(invitee=user))


class WiderGroupAccessRequestQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Don't have access
        if not user.is_authenticated:
            return
        if user.is_superuser or user.is_staff:
            return self.all()
        else:
            return self.filter(user=user)
            # return self.all()

class StoryReviewQuerySet(models.QuerySet):
    def for_user(self, user):
        # Not logged in? Don't have access
        if not user.is_authenticated:
            return
        if user.is_superuser or user.is_staff:
            return self.all()
        else:
            # return self.filter(user=user) | self.filter(Q(reviewer=user))
            return self.all()

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
    copyright_text = models.CharField(max_length=500, default=None, blank=True, null=True)
    assigned_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    uploaded_by = models.ForeignKey('auth.User', related_name='datasets', on_delete=models.CASCADE)
    shared_with = ArrayField(models.IntegerField(), default=None, blank=True, null=True)
    style = JSONField(default=None, blank=True, null=True)
    objects = DatasetQuerySet.as_manager()


class StoryType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.type


class Atua(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Story(models.Model):
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
    approx_time = JSONField(default=None, blank=True, null=True)
    atua =  models.ManyToManyField("Atua")
    story_type = models.ForeignKey(StoryType, blank=True, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='stories', on_delete=models.CASCADE)
    is_detectable = models.BooleanField(default=True, blank=True, null=True)
    last_edited_by = models.ForeignKey('auth.User', related_name="last_edited", blank=True, null=True, on_delete=models.CASCADE)
    being_edited_by = models.ForeignKey('auth.User', related_name="being_edited", blank=True, null=True, on_delete=models.CASCADE)
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
    def __str__(self):
        return self.type


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
    def __str__(self):
        return self.field_name


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)


# class TribalRegisterList(models.Model):
#     first_names = models.CharField(max_length=300)
#     last_name = models.CharField(max_length=300)
#     birth_date = models.DateField()
#     iwi = models.CharField(max_length=300, default='Ngāti Whakaue')
#     koromatua = models.CharField(max_length=300)
#     whanau = ArrayField(models.CharField(max_length=300))
#     membership_number = models.CharField(max_length=100)


class Sector(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Nest(models.Model):
    name = models.CharField(max_length=300)
    kinship_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    kaitiaki = models.ManyToManyField(User)
    created_by = models.ForeignKey('auth.User', related_name='creatednests', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    objects = NestQuerySet.as_manager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True)
    pepeha = models.TextField(max_length=2000, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    membership_number = models.CharField(max_length=100, blank=True, null=True)
    affiliation = models.ManyToManyField(Nest, related_name="members")
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    background_info = models.TextField(max_length=2000, blank=True, null=True)

class WhanauGroupInvitation(models.Model):
    nest = models.ForeignKey(Nest, related_name='invitations', on_delete=models.CASCADE)
    invitee = models.ForeignKey('auth.User', related_name='invitations', on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(blank=True, null=True)
    objects = WhanauGroupInvitationQuerySet.as_manager()

class WiderGroupAccessRequest(models.Model):
    nest = models.ForeignKey(Nest, related_name='accessrequests', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='accessrequests', on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(blank=True, null=True)
    accepted_by = models.ForeignKey('auth.User', related_name='grantedaccess', on_delete=models.CASCADE, blank=True, null=True)
    objects = WiderGroupAccessRequestQuerySet.as_manager()

class Publication(models.Model):
    STATUS = Choices(
        ('DRAFT', 'DRAFT'),
        ('SUBMITTED', 'SUBMITTED'),
        ('REVIEWED', 'REVIEWED'),
        ('ACCEPTED', 'ACCEPTED'),
        ('PUBLISHED', 'PUBLISHED'),
        ('UNPUBLISHED', 'UNPUBLISHED')
    )
    story = models.ForeignKey(Story, related_name='publications', on_delete=models.CASCADE)
    nest = models.ForeignKey(Nest, related_name='publications', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default=STATUS.SUBMITTED, null=False, choices=STATUS)
    status_modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'nest'], name='unique_story_nest')
        ]

class StoryReview(models.Model):
    publication = models.ForeignKey(Publication, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)
    reviewed_on = models.DateTimeField(auto_now_add=True)
    review = models.TextField(max_length=200,blank=True, null=True)
    objects = StoryReviewQuerySet.as_manager()
