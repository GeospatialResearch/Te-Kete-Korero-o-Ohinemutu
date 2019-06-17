# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
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
from .models import Dataset, PolygonEntity
from django.contrib.gis.geos import MultiPolygon, GEOSGeometry
from django.db import transaction
# import requests


# Util Functions
def get_layer_from_file(file_obj, directory):
    layer = None
    local_filename = os.path.join(directory, 'layer_file.zip')
    write_uploaded_file(file_obj, local_filename)

    try:
        if zipfile.is_zipfile(local_filename):
            # Try to guess the filename... this makes it magic
            filename = None
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

        else:
            ds = ogr.Open(local_filename)

        layer = ds.GetLayer(0)
        extent = layer.GetExtent()
        print(extent)

        # Get transformation to WGS84
        epsgCode = 4326
        sourceSR = layer.GetSpatialRef()
        print(sourceSR)
        targetSR = osr.SpatialReference()
        targetSR.ImportFromEPSG(epsgCode)
        coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)

        jsonLayer = {
            "type": "FeatureCollection",
            "features": []
        }

        print(layer.GetFeatureCount())
        for x in range(layer.GetFeatureCount()):
            if x % 500 == 0:
                print(x)
            feature = layer.GetFeature(x)
            geom = feature.GetGeometryRef()
            if x == 1:
                geomtype = geom.GetGeometryName()
            # Transform everything... just in case
            geom.Transform(coordTrans)
            jsonobj = feature.ExportToJson(as_object=True)
            jsonLayer['features'].append(jsonobj)

        # print (jsonLayer)

    except GDALException as e:
        print("Failed to read dataset with error {}".format(e))
        raise ParseError('Failed to read uploaded dataset.')

    fname, file_extension = os.path.splitext(filename)
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
        geomtypecode = 3
    elif geomtype == 'LINE' or geomtype == 'MULTILINE':
        geomtypecode = 2
    if geomtype == 'POINT':
        geomtypecode = 1
    print(geomtypecode)

    # create dataset record
    dataset = Dataset.objects.create(name=filename, geomtype=geomtypecode)
    dataset.save()

    for feature in geojson['features']:
        geom = GEOSGeometry(str(feature['geometry']))

        # Change the geometry to be a multipolygon
        if geom.geom_type == 'Polygon':
            geom = MultiPolygon([geom])

        PolygonEntity.objects.create(
            dataset=dataset,
            geom=geom,
            attributes=feature['properties']
        )

    # create geoserver layer from dataset inserted in database
    # done under the same transaction so the insert on database is rolled back
    # in case of error
    createGeoserverLayer(layer, dataset.id)


def createGeoserverLayer(layer, dataset_id=None):
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'password')
    gs_store = os.environ.get('GEOSERVER_DATASTORE', 'user_data')

    # curl -v -u admin:geoserver -GET -H "Accept: text/xml" http://localhost:8080/geoserver/rest/workspaces/storyapp
    # response = requests.get("http://geoserver:8080/geoserver/", auth=(gs_user, gs_pass))
    # print(response)

    cat = Catalog("http://geoserver:8080/geoserver/rest/", gs_user, gs_pass)
    store = cat.get_store(gs_store)

    geomtype = layer['geomtype']
    table = None
    if geomtype == 'POLYGON' or geomtype == 'MULTIPOLYGON':
        table = 'public.app_polygon_entity'
    elif geomtype == 'LINE' or geomtype == 'MULTILINE':
        table = 'public.app_line_entity'
    if geomtype == 'POINT':
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
        print(ft.__dict__)
        cat.save(ft)
    except Exception:
        raise
        print(sys.exc_info()[1])


# Create your views here.
class UploadFile(APIView):
    def post(self, request):
        # This will automatically clean up after us.
        with TemporaryDirectory() as directory:
            file_obj = request.data['file']
            layer = get_layer_from_file(file_obj, directory)

            insertDB(layer)

        return Response(layer['jsonlayer'])
