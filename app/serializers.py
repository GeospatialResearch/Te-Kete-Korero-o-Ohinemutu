from rest_framework.serializers import ModelSerializer, ListField, SerializerMethodField, JSONField, PrimaryKeyRelatedField, ReadOnlyField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Dataset, CoAuthor, Story, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation, Atua, StoryType, ContentType, Comment, Profile, Sector, Nest, WhanauGroupInvitation, Publication, WiderGroupAccessRequest
from django.contrib.gis.geos import GEOSGeometry
from rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.models import User

class DatasetSerializer(ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class AtuaSerializer(ModelSerializer):
    class Meta:
        model = Atua
        fields = '__all__'


class UserSerializer(ModelSerializer):
    profile = SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', )

    def get_profile(self, user):
        serializer = ProfileSimpleSerializer(instance=user.profile)
        return serializer.data


class UserSimpleSerializer(ModelSerializer):
    profile = SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'id', 'first_name', 'last_name', 'profile')

    def get_profile(self, user):
        serializer = ProfileSimpleSerializer(instance=user.profile)
        return serializer.data


class StoryTypeSerializer(ModelSerializer):
    class Meta:
        model = StoryType
        fields = '__all__'


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class StorySerializer(ModelSerializer):
    storyBodyElements_temp = ListField(write_only=True)
    atua_temp = PrimaryKeyRelatedField(write_only=True,many=True,queryset=Atua.objects.all())
    story_type_id = PrimaryKeyRelatedField(source="StoryType",queryset=StoryType.objects.all(),required=False)
    owner = ReadOnlyField(source='owner.username')
    being_edited_by = ReadOnlyField(source='being_edited_by.id')
    comments = SerializerMethodField()
    storyBodyElements = SerializerMethodField()
    story_type = StoryTypeSerializer(read_only=True)
    co_authors = SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('atua',)

    def get_comments(self, story):
        c = Comment.objects.filter(story=story).order_by('-date')
        serializer = CommentSerializer(instance=c, many=True)
        return serializer.data

    def get_storyBodyElements(self, story):
        sb = StoryBodyElement.objects.filter(story=story)
        serializer = StoryBodyElementSerializer(instance=sb, many=True)
        return serializer.data

    def get_co_authors(self, obj):
        authors=  CoAuthor.objects.filter(story=obj)
        return [author.co_author.id for author in authors]

    def create(self, validated_data):
        elements = validated_data.pop('storyBodyElements_temp')
        atuas = validated_data.pop('atua_temp')
        story_type_data = validated_data.pop('StoryType')

        story = Story.objects.create(**validated_data,story_type=story_type_data)

        for atua in atuas:
            story.atua.add(atua)
        for element in elements:
            if 'mediafile' in element:
                if element['mediafile'] is not None:
                    mediafile = MediaFile.objects.get(id=element['mediafile'])
                    element['mediafile'] = mediafile
            elif 'geom_attr' in element:
                if element['geom_attr'] is not None:
                    geomattr = StoryGeomAttrib.objects.get(id=element['geom_attr']['id'])
                    element['geom_attr'] = geomattr
            elif 'content_type' in element:
                if element['content_type']:
                    content_type = ContentType.objects.get(id=element['content_type'])
                    element['content_type'] = content_type

            StoryBodyElement.objects.create(story=story,**element)
        return story

    def update(self, instance, validated_data):
        storyBodyElements = validated_data.pop('storyBodyElements_temp')
        atuas = validated_data.pop('atua_temp')
        instance.story_type = validated_data.pop('StoryType')
        instance.atua.clear()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for atua in atuas:
            instance.atua.add(atua)


        for element in storyBodyElements:

            if 'story' in element:
                element.pop('story')

            if 'id' in element:
                if element['element_type'] in ['IMG', 'VIDEO', 'AUDIO']:
                    element.pop('mediafile')
                    element.pop('mediafile_name')
                elif element['element_type'] == 'GEOM':
                    element.pop('geom_attr')

                if 'content_type' in element:
                    if element['content_type']:
                        id = element['content_type']["id"] if "id" in element['content_type'] else element['content_type']
                        content_type = ContentType.objects.get(id=id)
                        element['content_type'] = content_type

                elem = StoryBodyElement.objects.get(id=element["id"])
                for attr, value in element.items():
                    setattr(elem, attr, value)
                elem.save()
            else:
                if element['element_type'] in ['IMG', 'VIDEO', 'AUDIO']:
                    if element['mediafile'] is not None:
                        mediafile = MediaFile.objects.get(id=element['mediafile'])
                        element['mediafile'] = mediafile
                elif element['element_type'] == 'GEOM':
                    if element['geom_attr'] is not None:
                        geomattr = StoryGeomAttrib.objects.get(id=element['geom_attr']['id'])
                        element['geom_attr'] = geomattr

                if 'content_type' in element:
                    if element['content_type']:
                        id = element['content_type']["id"] if "id" in element['content_type'] else element['content_type']
                        content_type = ContentType.objects.get(id=id)
                        element['content_type'] = content_type

                StoryBodyElement.objects.create(story=instance,**element)

        instance.save()
        return instance


class StorySimpleSerializer(ModelSerializer):
    owner = ReadOnlyField(source='user.username')

    class Meta:
        model = Story
        fields = ('id', 'title', 'summary', 'story_type', 'owner')
        depth = 1

class MediaFileSerializer(ModelSerializer):

    size = SerializerMethodField()
    name = SerializerMethodField()
    filetype = SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = ('id', 'file', 'size', 'name', 'filetype')

    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size

    def get_name(self, obj):
        file_name = ''
        if obj.file and hasattr(obj.file, 'name'):
            file_name = obj.file.name
        return file_name

    def get_filetype(self, obj):
      filename = obj.file.name
      return filename.split('.')[-1]


class StoryGeomAttribMediaSerializer(ModelSerializer):
    mediafile_temp = PrimaryKeyRelatedField(write_only=True, queryset=MediaFile.objects.all())
    geomattr_temp = PrimaryKeyRelatedField(write_only=True, queryset=StoryGeomAttrib.objects.all())

    class Meta:
        model = StoryGeomAttribMedia
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        mediafile = validated_data.pop('mediafile_temp')
        geom_attr = validated_data.pop('geomattr_temp')

        storyGeomAttribMedia = StoryGeomAttribMedia.objects.create(**validated_data, mediafile=mediafile, geom_attr=geom_attr)
        return storyGeomAttribMedia


class StoryGeomAttribSerializer(ModelSerializer):
    geomAttribMedia = SerializerMethodField()

    class Meta:
        model = StoryGeomAttrib
        fields = '__all__'
        depth = 3

    def get_geomAttribMedia(self, geomAttr):
        gm = StoryGeomAttribMedia.objects.filter(geom_attr=geomAttr)
        serializer = StoryGeomAttribMediaSerializer(instance=gm, many=True)
        return serializer.data

    def create(self, validated_data):
        GEOSgeom = GEOSGeometry(str(validated_data['geometry']))
        validated_data['geometry'] = GEOSgeom
        storyGeomAttrib = StoryGeomAttrib.objects.create(**validated_data)
        return storyGeomAttrib

    def update(self, instance, validated_data):
        GEOSgeom = GEOSGeometry(str(validated_data['geometry']))
        validated_data['geometry'] = GEOSgeom

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StoryBodyElementSerializer(ModelSerializer):
    geom_attr = StoryGeomAttribSerializer()
    story = StorySimpleSerializer()

    class Meta:
        model = StoryBodyElement
        fields = '__all__'


class WebsiteTranslationSerializer(ModelSerializer):

    class Meta:
        model = WebsiteTranslation
        fields = '__all__'


# used to replace django contrib admin template of email message
class CustomPasswordResetSerializer(PasswordResetSerializer):

    # password_reset_form_class = CustomResetPasswordForm

    def get_email_options(self):
        request = self.context.get('request')
        host = str(request.get_host()).split(":", 1)[0]
        if 'api' in host:
            host = host.replace("api", "www")
        return {
            'domain_override': host,
            'html_email_template_name': 'account/email/password_reset_html_email.html'
        }


class CommentSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'


class CoAuthorSerializer(ModelSerializer):
    story_id = PrimaryKeyRelatedField(source="story",queryset=Story.objects.all(),required=False)
    co_author = ListField(write_only=True)

    class Meta:
        model = CoAuthor
        fields = ('id', 'story_id', 'co_author')

    def create(self, validated_data):
        story = validated_data.pop('story')
        authors =  validated_data.pop('co_author')
        CoAuthor.objects.filter(story=story).delete()
        for author in authors:
            CoAuthor.objects.create(story=story,co_author_id=author)
        return CoAuthor.objects.filter(story=story).all()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSimpleSerializer(ModelSerializer):
    username = ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ('user_id', 'avatar', 'username', 'background_info', 'phone_number')



class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class NestSimpleSerializer(ModelSerializer):
    kinship_sector = SectorSerializer(read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    class Meta:
        model = Sector
        fields = '__all__'


class NestSerializer(ModelSerializer):
    kaitiaki_temp = PrimaryKeyRelatedField(write_only=True, many=True, queryset=User.objects.all(), required=False, allow_null=True, default=None)
    kinship_sector_id = PrimaryKeyRelatedField(source="Sector",queryset=Sector.objects.all(),required=False)
    kinship_sector = SectorSerializer(read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    kaitiaki = UserSimpleSerializer(read_only=True, many=True)
    members = SerializerMethodField()
    invitations = SerializerMethodField()
    accessrequests = SerializerMethodField()
    publications = SerializerMethodField()

    class Meta:
        model = Nest
        fields = '__all__'
        depth = 1

    def get_members(self, nest):
        members = nest.members.all()
        serializer = ProfileSimpleSerializer(instance=members, many=True)
        return serializer.data

    def get_invitations(self, nest):
        invitations = nest.invitations.all()
        serializer = WhanauGroupInvitationSerializer(instance=invitations, many=True)
        return serializer.data

    def get_accessrequests(self, nest):
        accessrequests = nest.accessrequests.all()
        serializer = WiderGroupAccessRequestSerializer(instance=accessrequests, many=True)
        return serializer.data

    def get_publications(self, nest):
        number_publications = nest.publications.all().count()
        return number_publications

    def create(self, validated_data):
        validated_data.pop('kaitiaki_temp')
        kinship_sector = validated_data.pop('Sector')
        nest = Nest.objects.create(**validated_data, kinship_sector=kinship_sector)
        return nest


    def update(self, instance, validated_data):
        instance.kinship_sector = validated_data.pop('Sector')
        kaitiaki = validated_data.pop('kaitiaki_temp')

        instance.kaitiaki.clear()
        for k in kaitiaki:
            instance.kaitiaki.add(k)
        instance.name = validated_data['name']

        instance.save()
        return instance


class WhanauGroupInvitationSerializer(ModelSerializer):
    invitee_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    nest_id = PrimaryKeyRelatedField(queryset=Nest.objects.all())
    nest = NestSimpleSerializer(read_only=True)
    invitee = UserSimpleSerializer(read_only=True)

    class Meta:
        model = WhanauGroupInvitation
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        invitee = validated_data.pop('invitee_id')
        nest = validated_data.pop('nest_id')
        invitation = WhanauGroupInvitation.objects.create(invitee=invitee, nest=nest)
        return invitation

class WiderGroupAccessRequestSerializer(ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    user = UserSimpleSerializer(read_only=True)

    nest_id = PrimaryKeyRelatedField(queryset=Nest.objects.all(), required=False)
    nest = NestSimpleSerializer(read_only=True)

    accepted_by_id = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    accepted_by = UserSimpleSerializer(read_only=True)

    nests = ListField(write_only=True)
    class Meta:
        model = WiderGroupAccessRequest
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        user = validated_data.pop('user_id')
        nest = validated_data.pop('nests')
        accessrequest = None
        # accepted_by = validated_data.pop('accepted_by_id')
        for nes in nest:
            accessrequest = WiderGroupAccessRequest.objects.create(user_id=user.id, nest_id=nes)
        return accessrequest

    def update(self, instance, validated_data):
        accepted_by= validated_data.pop('accepted_by_id')
        accepted= validated_data.pop('accepted')
        instance.accepted = accepted
        instance.accepted_by = accepted_by
        instance.save()
        return instance

class PublicationSerializer(ModelSerializer):
    nest = NestSerializer()

    class Meta:
        model = Publication
        fields = '__all__'
        depth = 1
