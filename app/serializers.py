from rest_framework.serializers import ModelSerializer, ListField, SerializerMethodField, JSONField, PrimaryKeyRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Dataset, Story, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation, Atua, StoryType, ContentType
from django.contrib.gis.geos import GEOSGeometry


class DatasetSerializer(ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'


class AtuaSerializer(ModelSerializer):
    class Meta:
        model = Atua
        fields = '__all__'



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

    storyBodyElements = SerializerMethodField()
    story_type = StoryTypeSerializer(read_only=True)

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('atua',)

    def get_storyBodyElements(self, story):
        sb = StoryBodyElement.objects.filter(story=story)
        serializer = StoryBodyElementSerializer(instance=sb, many=True)
        return serializer.data

    def create(self, validated_data):
        elements = validated_data.pop('storyBodyElements_temp')
        atuas = validated_data.pop('atua_temp')
        story_type_data =  validated_data.pop('StoryType')

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

    class Meta:
        model = StoryBodyElement
        fields = '__all__'
        depth = 3


class WebsiteTranslationSerializer(ModelSerializer):

    class Meta:
        model = WebsiteTranslation
        fields = '__all__'
