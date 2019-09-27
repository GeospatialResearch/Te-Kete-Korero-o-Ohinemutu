from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Dataset, Story, StoryGeomAttrib, StoryPointGeom, StoryLineGeom, StoryPolygonGeom, StoryBody

class DatasetSerializer(ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'


class StorySerializer(ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'


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
