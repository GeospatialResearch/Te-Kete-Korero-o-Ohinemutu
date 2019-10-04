from rest_framework.serializers import ModelSerializer,ListField,SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Dataset, Story, StoryGeomAttrib, StoryPointGeom, StoryLineGeom, StoryPolygonGeom, StoryBodyElement, MediaFile

class DatasetSerializer(ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'


class StorySerializer(ModelSerializer):
    storyBodyElements_temp = ListField(write_only=True)
    # storyGeomsAttrib_temp = ListField(write_only=True)
    storyBodyElements = SerializerMethodField()
    storyGeomsAttrib = SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'

    def get_storyBodyElements(self, story):
        sb = StoryBodyElement.objects.filter(story=story)
        serializer = StoryBodyElementSerializer(instance=sb, many=True)
        return serializer.data

    def get_storyGeomsAttrib(self, story):
        sg = StoryGeomAttrib.objects.filter(story=story)
        serializer = StoryGeomAttribSerializer(instance=sg, many=True)
        return serializer.data

    def create(self, validated_data):
        print(validated_data)
        elements = validated_data.pop('storyBodyElements_temp')
        print(elements)
        story = Story.objects.create(**validated_data)
        for element in elements:
            if 'mediafile' in element:
                if element['mediafile'] is not None:
                    mediafile = MediaFile.objects.get(id=element['mediafile'])
                    element['mediafile'] = mediafile

            StoryBodyElement.objects.create(story=story,**element)
        return story

    def update(self, instance, validated_data):
        storyBodyElements = validated_data.pop('storyBodyElements_temp')
        # storyGeomsAttrib = validated_data.pop('storyGeomsAttrib_temp')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for element in storyBodyElements:
            if 'id' in element:
                element.pop('mediafile')
                element.pop('mediafile_name')

                elem = StoryBodyElement.objects.get(id=element["id"])
                for attr, value in element.items():
                    setattr(elem, attr, value)
                elem.save()
            else:
                if 'mediafile' in element:
                    if element['mediafile'] is not None:
                        mediafile = MediaFile.objects.get(id=element['mediafile'])
                        element['mediafile'] = mediafile
                StoryBodyElement.objects.create(story=instance,**element)

        instance.save()
        return instance
        

class StoryBodyElementSerializer(ModelSerializer):
    class Meta:
        model = StoryBodyElement
        exclude = ('story',)
        depth = 1


class MediaFileSerializer(ModelSerializer):

    size = SerializerMethodField()
    name = SerializerMethodField()
    filetype = SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = ('id', 'file', 'size', 'name', 'filetype')
        depth = 1

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


class StoryGeomAttribSerializer(ModelSerializer):

    class Meta:
        model = StoryGeomAttrib
        exclude = ('story',)
        depth = 1


class StoryPointGeomSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = StoryPointGeom
        geo_field = 'geom'
        fields = '__all__'
        depth = 1


class StoryLineGeomSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = StoryLineGeom
        geo_field = 'geom'
        fields = '__all__'
        depth = 1


class StoryPolygonGeomSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = StoryPolygonGeom
        geo_field = 'geom'
        fields = '__all__'
        depth = 1
