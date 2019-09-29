from rest_framework.serializers import ModelSerializer,ListField,SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Dataset, Story, StoryGeomAttrib, StoryPointGeom, StoryLineGeom, StoryPolygonGeom, StoryBody

class DatasetSerializer(ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'


class StorySerializer(ModelSerializer):
    elements = ListField(write_only=True)
    storyBodies = SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'#('created_date','modified_date','title','summary','status','storyBodies', 'elements')

    def get_storyBodies(self, story):
        sb = StoryBody.objects.filter( story=story)
        serializer = StoryBodySerializer(instance=sb, many=True)
        return serializer.data

    def create(self, validated_data):
        elements = validated_data.pop('elements')
        story = Story.objects.create(**validated_data)
        for element in elements:
            StoryBody.objects.create(story=story,**element)
        return story

class StoryBodySerializer(ModelSerializer):
    class Meta:
        model = StoryBody
        fields = '__all__'


class StoryGeomAttribSerializer(ModelSerializer):

    class Meta:
        model = StoryGeomAttrib
        fields = '__all__'
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
