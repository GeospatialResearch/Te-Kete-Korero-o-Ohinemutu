# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import DatasetSerializer
from django.http import JsonResponse
from .models import Dataset, PolygonEntity, LineEntity, PointEntity
from rest_framework.exceptions import ParseError
from django.contrib.gis.gdal.error import GDALException
from tempfile import TemporaryDirectory
import zipfile
import os
import sys
from osgeo import ogr
from osgeo import osr
from geoserver.catalog import Catalog
from geoserver.support import JDBCVirtualTable
from django.contrib.gis.geos import MultiPolygon, MultiLineString, MultiPoint, GEOSGeometry, WKTWriter
from django.db import transaction
import re

# Util Functions
def get_layer_from_file(file_obj, directory):
    layer = None
    local_filename = os.path.join(directory, 'layer_file.zip')
    write_uploaded_file(file_obj, local_filename)
    filename = None
    try:
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

            ds = ogr.Open('/vsizip/' + local_filename + '/' + filename)
            fname, file_extension = os.path.splitext(filename)

        else:
            ds = ogr.Open(local_filename)
            fname, file_extension = os.path.splitext(str(file_obj))

        # Get layer from ds
        layer = ds.GetLayer()
        print(layer.GetExtent())
        print(layer.GetFeatureCount())
        print(layer.GetSpatialRef())

        # Do some validation
        try:
            dataset = Dataset.objects.get(name = fname)
        except Dataset.DoesNotExist:
            dataset = None
        if dataset:
            raise ValidationError("Resource named " + fname + " already exists.")
        if not re.match("^[a-zA-Z0-9_-]*$", fname):
            raise ValidationError("The dataset name " + fname + " is invalid. Make sure the name does not have special characters and there are no subfolders in the uploaded dataset.")
        numberFeaturesLimit = 50000
        if layer.GetFeatureCount() > numberFeaturesLimit:
            raise ValidationError("The dataset "+ fname +" has " + str(format(layer.GetFeatureCount(), ',')) + " features. Please, upload a dataset with no more than " + str(format(numberFeaturesLimit, ',')) + " features.")
        if not layer.GetSpatialRef():
            raise ValidationError("Could not determine the Spatial Reference of the dataset.")

        # Get transformation to WGS84
        epsgCode = 4326
        sourceSR = layer.GetSpatialRef()
        # print(sourceSR)
        targetSR = osr.SpatialReference()
        targetSR.ImportFromEPSG(epsgCode)
        coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)

        jsonLayer = {
            "type": "FeatureCollection",
            "features": []
        }

        for x in range(layer.GetFeatureCount()):
            # if x % 2000 == 0:
            #     print(x)
            feature = layer.GetFeature(x)

            try:
                geom = feature.GetGeometryRef()
            except Exception as e:
                raise ValidationError("Please, upload a zipped shapefile or geojson file.")

            # Remove Z coord
            geom.FlattenTo2D()

            # Get geometry type
            if x == 1:
                geomtype = geom.GetGeometryName()
                print(geomtype)

            # Transform everything... just in case
            geom.Transform(coordTrans)
            jsonobj = feature.ExportToJson(as_object=True)
            jsonLayer['features'].append(jsonobj)

    except GDALException as e:
        print("Failed to read dataset with error {}".format(e))
        raise ParseError('Failed to read uploaded dataset.')

    return {'filename': fname, 'jsonlayer': jsonLayer, 'geomtype': geomtype}


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
    geojson = layer['jsonlayer']
    geomtype = layer['geomtype']

    geomtypecode = None
    if geomtype == 'POLYGON' or geomtype == 'MULTIPOLYGON':
        geomtypecode = Dataset.POLYGON
    elif geomtype == 'LINESTRING' or geomtype == 'MULTILINESTRING':
        geomtypecode = Dataset.LINE
    if geomtype == 'POINT' or geomtype == 'MULTIPOINT':
        geomtypecode = Dataset.POINT

    # create dataset record
    dataset = Dataset.objects.create(name=filename, geomtype=geomtypecode)
    dataset.save()
    print("######### Created dataset record #########")

    for feature in geojson['features']:
        geom = GEOSGeometry(str(feature['geometry']))

        # Change the geometry to be a multi
        if geom.geom_type == 'Polygon' or geom.geom_type == 'MultiPolygon':
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon([geom])
            PolygonEntity.objects.create(
                dataset=dataset,
                geom=geom,
                attributes=feature['properties']
            )
        elif geom.geom_type == 'LineString' or geom.geom_type == 'MultiLineString':
            if geom.geom_type == 'LineString':
                geom = MultiLineString([geom])
            LineEntity.objects.create(
                dataset=dataset,
                geom=geom,
                attributes=feature['properties']
            )
        elif geom.geom_type == 'Point' or geom.geom_type == 'MultiPoint':
            if geom.geom_type == 'Point':
                geom = MultiPoint([geom])
            PointEntity.objects.create(
                dataset=dataset,
                geom=geom,
                attributes=feature['properties']
            )

    print("######### Created polygons records #########")

    # create geoserver layer from dataset inserted in database
    # done under the same transaction so the insert on database is rolled back
    # in case of error
    createGeoserverLayer(layer, dataset.id)


def createGeoserverLayer(layer, dataset_id=None):
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'password')
    gs_workspace = os.environ.get('GEOSERVER_WORKSPACE', 'storyapp')
    gs_store = os.environ.get('GEOSERVER_DATASTORE', 'user_data')

    cat = Catalog("http://geoserver:8080/geoserver/rest/", gs_user, gs_pass)
    workspace = cat.get_workspace(gs_workspace)
    store = cat.get_store(gs_store, workspace)

    geomtype = layer['geomtype']
    print(geomtype)
    table = None
    if geomtype == 'POLYGON' or geomtype == 'MULTIPOLYGON':
        table = 'public.app_polygon_entity'
    elif geomtype == 'LINESTRING' or geomtype == 'MULTILINESTRING':
        table = 'public.app_line_entity'
    if geomtype == 'POINT' or geomtype == 'MULTIPOINT':
        table = 'public.app_point_entity'

    ft_name = layer['filename']
    epsg_code = 'EPSG:4326'
    sql = "select id, geom from " + table + " where dataset_id = '" + str(dataset_id) + "'"
    geom = None
    keyColumn = None
    parameters = None

    try:
        jdbc_vt = JDBCVirtualTable(ft_name, sql, 'false', geom, keyColumn, parameters)
        ft = cat.publish_featuretype(ft_name, store, epsg_code, jdbc_virtual_table=jdbc_vt)
        print("######### Published Geoserver layer #########")
        cat.save(ft)
    except Exception as e:
        print(e)
        raise ValidationError(e)


# Create your views here.
class UploadFileView(APIView):
    def post(self, request):

        # This will automatically clean up after us.
        with TemporaryDirectory() as directory:
            file_obj = request.data['file']
            layer = get_layer_from_file(file_obj, directory)

            insertDB(layer)

        return Response(layer)


## ViewSets are particularly useful for CRUD APIs
## (grouping operations on the same resource minimizing the amount of code you need to write and generating urls behind the scene)
## to be used with urls.py through router.register(r'datasets', views.DatasetViewSet)
class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()


def dataset_list(request):
    if request.method == 'GET':
        datasets = Dataset.objects.all().values('name')
        datasets_list = list(datasets)
        return JsonResponse(datasets_list, safe=False)


def spatial_features(request):
    id = request.GET.get('id', None)
    geomtype = request.GET.get('geomtype', None)

    if id is not None:
        if geomtype == 'Polygon' or geomtype == 'MultiPolygon':
            feature = PolygonEntity.objects.get(id=id)
        if geomtype == 'LineString' or geomtype == 'MultiLineString':
            feature = LineEntity.objects.get(id=id)
        if geomtype == 'Point' or geomtype == 'MultiPoint':
            feature = PointEntity.objects.get(id=id)

    return JsonResponse(feature.attributes)
