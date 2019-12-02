# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.decorators import detail_route
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import DatasetSerializer, StorySerializer, StoryGeomAttribSerializer, StoryBodyElementSerializer, MediaFileSerializer, StoryGeomAttribMediaSerializer, WebsiteTranslationSerializer, AtuaSerializer, StoryTypeSerializer, ContentTypeSerializer
from django.http import JsonResponse
from .models import Dataset, Story, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation, Atua, StoryType, ContentType
from tempfile import TemporaryDirectory
import zipfile
import os
from osgeo import ogr
from geoserver.catalog import Catalog
from django.db import transaction
import re
from .utils import layer_type, get_catalog
import requests
from django.utils import timezone

# Util Functions
def get_layer_from_file(file_obj, directory):
    layer = None
    local_filename = os.path.join(directory, 'layer_file.zip')
    write_uploaded_file(file_obj, local_filename)

    # Get the type of dataset (vector ot raster)
    if zipfile.is_zipfile(local_filename):
        the_type = layer_type(local_filename)
    else:
        the_type = layer_type(str(file_obj))

    if the_type is None:
        raise ValidationError("Please, upload a valid dataset. The dataset is not a raster neither a vector.")

    elif the_type == 'vector':
        filename = None
        if zipfile.is_zipfile(local_filename):
            # Try to guess the filename... this makes it magic
            biggest_file_size = 0
            with zipfile.ZipFile(local_filename) as myzip:
                inner_files = myzip.namelist()
                if len(inner_files) == 1:
                    filename = inner_files[0]
                for file in inner_files:
                    if os.path.splitext(file)[1][1:] in ['shp', 'tab', 'SHP', 'TAB']:
                        filename = file
                        break
                    else:
                        if myzip.getinfo(file).file_size > biggest_file_size:
                            filename = file
                            biggest_file_size = myzip.getinfo(file).file_size

            #Get vector dataset
            ds = ogr.Open('/vsizip/' + local_filename + '/' + filename)
            fname, file_extension = os.path.splitext(filename)

        else:
            raise ValidationError("Please, upload a zipped vector dataset.")

        # Get layer from ds for validation purposes
        try:
            layer = ds.GetLayer()
        except Exception as e:
            raise ValidationError("Could not get the data from the dataset. Please, upload a zipped dataset.")

        # Do some validation
        try:
            dataset = Dataset.objects.get(name = fname)
        except Dataset.DoesNotExist:
            dataset = None
        if dataset:
            raise ValidationError("Resource named " + fname + " already exists.")
        if fname[0].isdigit():
            raise ValidationError("The dataset name can't start with a digit. Please make sure the dataset name starts with an alpha character.")
        if not re.match("^[a-zA-Z0-9_-]*$", fname):
            raise ValidationError("The dataset name " + fname + " is invalid. Make sure the name does not have any spaces or special characters and there are no subfolders in the uploaded dataset.")
        numberFeaturesLimit = 50000
        if layer.GetFeatureCount() > numberFeaturesLimit:
            raise ValidationError("The dataset "+ fname +" has " + str(format(layer.GetFeatureCount(), ',')) + " features. Please, upload a dataset with no more than " + str(format(numberFeaturesLimit, ',')) + " features.")
        if not layer.GetSpatialRef():
            raise ValidationError("Could not determine the Spatial Reference of the dataset. Please, upload a zipped shapefile.")

        # Get geometry type
        feature = layer.GetFeature(0)
        try:
            geom = feature.GetGeometryRef()
        except:
            raise ValidationError("Could not determine the geometries of the dataset. Please, upload a zipped shapefile.")
        geomtype = geom.GetGeometryName()

        return {'filename': fname, 'extension': file_extension, 'localfilename': local_filename, 'geomtype': geomtype}


    elif the_type == 'raster':
        filename = None
        if zipfile.is_zipfile(local_filename):
            # Try to guess the filename... this makes it magic
            biggest_file_size = 0
            with zipfile.ZipFile(local_filename) as myzip:
                inner_files = myzip.namelist()
                if len(inner_files) == 1:
                    filename = inner_files[0]
                for file in inner_files:
                    if os.path.splitext(file)[1][1:] in ['shp', 'tab', 'SHP', 'TAB']:
                        filename = file
                        break
                    else:
                        if myzip.getinfo(file).file_size > biggest_file_size:
                            filename = file
                            biggest_file_size = myzip.getinfo(file).file_size

            fname, file_extension = os.path.splitext(filename)
        else:
            fname, file_extension = os.path.splitext(str(file_obj))

        if not re.match("^[a-zA-Z0-9_-]*$", fname):
            raise ValidationError("The dataset name " + fname + " is invalid. Make sure the name does not have any spaces or special characters and there are no subfolders in the uploaded dataset.")
        if fname[0].isdigit():
            raise ValidationError("The dataset name can't start with a digit. Please make sure the dataset name starts with an alpha character.")
        if zipfile.is_zipfile(local_filename):
            raise ValidationError('Please, upload a raster file with .tif format instead of a zipped folder.')

        return {'filename': fname, 'extension': file_extension, 'localfilename': local_filename, 'geomtype': the_type}


def write_uploaded_file(in_file, destination):
    with open(destination, 'wb') as out_file:
        for chunk in in_file.chunks():
            out_file.write(chunk)


def getEPSG(layer):
    # Load in the projection WKT
    sr = layer.GetSpatialRef()
    # Try to determine the EPSG/SRID code
    res = sr.AutoIdentifyEPSG()
    if res == 0:  # success
        print('SRID=' + sr.GetAuthorityCode(None))
    else:
        print('Could not determine SRID')


@transaction.atomic
def insertDB(layer):
    filename = layer['filename']
    geomtype = layer['geomtype']

    geomtypecode = None
    if geomtype == 'POLYGON' or geomtype == 'MULTIPOLYGON':
        geomtypecode = Dataset.POLYGON
    elif geomtype == 'LINESTRING' or geomtype == 'MULTILINESTRING':
        geomtypecode = Dataset.LINE
    elif geomtype == 'POINT' or geomtype == 'MULTIPOINT':
        geomtypecode = Dataset.POINT
    elif geomtype == 'raster':
        geomtypecode = Dataset.RASTER

    # create dataset record
    dataset = Dataset.objects.create(name=filename, geomtype=geomtypecode)
    dataset.save()
    print("######### Created dataset record #########")

    if geomtype == 'raster':
        createGeoserverCoverageLayer(layer)
    else:
        createGeoserverShpLayer(layer)


def createGeoserverShpLayer(layer, dataset_id=None):
    """Creates a datastore of type Shapefile and a FeatureType layer in GeoServer
    using GeoServer REST API through the Python requests module"""
    cat = get_catalog()
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')

    local_filename = layer['localfilename']
    filename = layer['filename']
    file_extension = layer['extension']

    if file_extension != '.shp':
        raise ValidationError("Please, upload a zipped shapefile instead of a {} file".format(file_extension))

    headers_zip = {'content-type': 'application/zip'}
    with open(local_filename, 'rb') as zip_file:
            r_create_layer = requests.put("http://geoserver:8080/geoserver/rest/workspaces/storyapp/datastores/" + filename + "/file.shp?charset=utf-8",
                auth=(gs_user, gs_pass),
                data=zip_file,
                headers=headers_zip)
            try:
                r_create_layer.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise ValidationError(e)
            if r_create_layer.status_code == 200:
                print("######### Published Geoserver shp datastore and layer#########")

            cat.reload()
            resource = cat.get_resource(layer['filename'])
            if resource.projection is None:
                delete_layer(layer['filename'])
                raise ValidationError("The dataset does not have a defined projection. Please insert a valid dataset.")


def createGeoserverCoverageLayer(layer):
    """Creates a datastore of type GeoTIFF and a Coverage layer in GeoServer
    using GeoServer REST API through gsconfig.py"""
    cat = get_catalog()
    resource = cat.get_resource(layer['filename'])

    file_extension = layer['extension']

    if file_extension != '.tif':
        raise ValidationError("Please, upload a raster dataset with .tif instead of a {} file".format(file_extension))

    try:
        if resource is not None:
            cat.create_coveragestore(layer['filename'], layer['localfilename'])
        else:
            cat.create_coveragestore(layer['filename'], layer['localfilename'], overwrite=True)
        print("######### Created Geoserver coverage #########")

    except Exception as e:
        if str(e) == 'Could not aquire reader for coverage.':
            raise ValidationError(str(e) + " Please, convert your raster file into .tif format.")
        else:
            raise ValidationError(e)

    cat.reload()
    resource = cat.get_resource(layer['filename'])
    if resource.projection is None:
        delete_layer(layer['filename'])
        raise ValidationError("The dataset does not have a defined projection. Please insert a valid dataset.")


@transaction.atomic
def delete_layer(layername):
    # Remove from database
    Dataset.objects.get(name=layername).delete()

    # Remove from GeoServer
    cat = get_catalog()

    store = cat.get_store(layername)
    if store.type == 'Shapefile' or store.type == 'PostGIS':
        storetype = 'datastores'
    elif store.type == 'GeoTIFF':
        storetype = 'coveragestores'

    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')
    r_detele = requests.delete("http://geoserver:8080/geoserver/rest/workspaces/storyapp/" + storetype + "/" + layername + "?recurse=true",
        auth=(gs_user, gs_pass))
    try:
        r_detele.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValidationError(e)

    cat.reload()
    style = cat.get_style("style_" + layername)
    if style is not None:
        cat.delete(style)


class GetGeoServerDefaultStyle(APIView):
    def get(self, request):
        layername = request.GET.get('layername', None)

        cat = get_catalog()

        layer = cat.get_layer(layername)
        sld = layer.default_style.sld_body

        return Response( { 'sld': sld, 'stylename': layer.default_style.name })


class SetGeoServerDefaultStyle(APIView):
    def post(self, request):
        layername = request.data['layername']
        sld = request.data['sld']

        cat = get_catalog()

        layer = cat.get_layer(layername)
        newstyle = cat.create_style('style_' + layername, sld, overwrite=True)
        layer.default_style = 'style_' + layername
        cat.save(layer)

        return Response({'result': None})


class UploadFileView(APIView):
    def post(self, request):

        # This will automatically clean up after us.
        with TemporaryDirectory() as directory:
            file_obj = request.data['file']
            layer = get_layer_from_file(file_obj, directory)

            if layer is not None:
                insertDB(layer)

        return Response(layer)


# https://www.techiediaries.com/django-rest-image-file-upload-tutorial/
class UploadMediaFileView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = MediaFileSerializer(data=request.data)

        # Make some validation on media file format
        img_exts = ['.jpg', '.jpeg', '.png', '.svg', '.bmp']
        video_exts = ['.mp4']
        audio_exts = ['.mp3']
        filename = str(request.data['file'])
        base_name, ext = os.path.splitext(filename)
        if ext.lower() not in img_exts and ext.lower() not in video_exts and ext.lower() not in audio_exts:
            raise ValidationError("The format of the media file " + filename + " is not supported. Please, upload a media file with one of the following extensions: " + ",".join(img_exts) + "," + ",".join(video_exts) + " and" + ",".join(audio_exts))

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleanMediaFilesView(APIView):

    def post(self, request):
        mediafiles = MediaFile.objects.all()

        used_mediafiles = StoryBodyElement.objects.values_list('mediafile_name', flat=True)
        used_mediafiles = list(used_mediafiles)

        used_mediafiles_geomAttrMedia = StoryGeomAttribMedia.objects.values_list('mediafile_name', flat=True)
        used_mediafiles_geomAttrMedia = list(used_mediafiles_geomAttrMedia)

        hours_threshold = 4
        seconds_threshold = hours_threshold * 60 * 60

        for mediafile in mediafiles:
            if str(mediafile.file) not in used_mediafiles and str(mediafile.file) not in used_mediafiles_geomAttrMedia:
                delta = timezone.now() - mediafile.created_date
                # Condition to avoid deleting mediafiles that are being assigned for the first time on story editing (concurrent execution)
                if delta.total_seconds() > seconds_threshold:
                    mediafile.file.delete() # Deletes file from filesystem
                    mediafile.delete() # Deletes record

        return Response({'result': None})


class CleanGeomsView(APIView):

    def post(self, request):
        geomAttrs = StoryGeomAttrib.objects.all()

        used_geomattrs = StoryBodyElement.objects.values_list('geom_attr', flat=True)
        used_geomattrs = list(used_geomattrs)

        hours_threshold = 4
        seconds_threshold = hours_threshold * 60 * 60

        for geomattr in geomAttrs:
            if geomattr.id not in used_geomattrs:
                delta = timezone.now() - geomattr.created_date
                # Condition to avoid deleting geomattrs that are being assigned for the first time on story editing (concurrent execution)
                if delta.total_seconds() > seconds_threshold:
                    geomattr.delete()

        return Response({'result': None})


## ViewSets are particularly useful for CRUD APIs
## (grouping operations on the same resource minimizing the amount of code you need to write and generating urls behind the scene)
## to be used with urls.py through router.register(r'datasets', views.DatasetViewSet)
class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()
    

class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()

    def perform_create(self,serializer):
        serializer.save()
    def perform_update(self,serializer):
        serializer.save()


class StoryBodyElementViewSet(viewsets.ModelViewSet):
    serializer_class = StoryBodyElementSerializer
    queryset = StoryBodyElement.objects.all()

    def get_queryset(self):
        # If required, filter for the geom
        geomattr = self.request.query_params.get('geomattr', None)
        if geomattr is not None:
            queryset = self.queryset.filter(geom_attr=geomattr)
            return queryset

        return self.queryset


class AtuaViewSet(viewsets.ModelViewSet):
    serializer_class = AtuaSerializer
    queryset = Atua.objects.all()


class StoryTypeViewSet(viewsets.ModelViewSet):
    serializer_class = StoryTypeSerializer
    queryset = StoryType.objects.all()


class ContentTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()


class StoryGeomAttribViewSet(viewsets.ModelViewSet):
    serializer_class = StoryGeomAttribSerializer
    queryset = StoryGeomAttrib.objects.all()

    def perform_create(self,serializer):
        print("&&&&&&&&&&&&&&&&&&&&&&")
        serializer.save()
    def perform_update(self,serializer):
        serializer.save()


class StoryGeomAttribMediaViewSet(viewsets.ModelViewSet):
    serializer_class = StoryGeomAttribMediaSerializer
    queryset = StoryGeomAttribMedia.objects.all()

    def perform_create(self,serializer):
        serializer.save()

class MediaFileViewSet(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    queryset = MediaFile.objects.all()

class WebsiteTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WebsiteTranslationSerializer
    queryset = WebsiteTranslation.objects.all()


def dataset_list(request):
    if request.method == 'GET':
        datasets = Dataset.objects.all().values('name', 'geomtype', 'assigned_name')
        datasets_list = list(datasets)
        return JsonResponse(datasets_list, safe=False)


class DeleteLayer(APIView):
    def post(self, request):
        layername = request.data['layername']

        if layername is not None:
            delete_layer(layername)

        return Response({'result': None})


class RenameLayer(APIView):
    def post(self, request):
        layername = request.data['layername']
        assignedname = request.data['assignedName']

        if layername is not None and assignedname is not None:
            dataset = Dataset.objects.get(name=layername)
            dataset.assigned_name = assignedname
            dataset.save()

        return Response({'result': None})


def get_layer_bbox(request):
    layername = request.GET.get('layername', None)
    cat = get_catalog()
    if layername is not None:
        resource = cat.get_resource(layername)

    return JsonResponse({'bbox': resource.latlon_bbox})
