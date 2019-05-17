from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.gdal.error import GDALException
from tempfile import TemporaryDirectory
import zipfile
import os
from osgeo import ogr
from osgeo import osr


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

        shape = ds.GetLayer(0)
        extent = shape.GetExtent()
        print (extent)

        # Get transformation to Web Mercator
        epsgCode = 3857
        sourceSR = shape.GetSpatialRef()
        targetSR = osr.SpatialReference()
        targetSR.ImportFromEPSG(epsgCode)
        coordTrans = osr.CoordinateTransformation(sourceSR,targetSR)

        jsonLayer = {
            "type": "FeatureCollection",
            "features": []
        }

        print(shape.GetFeatureCount())
        for x in range(shape.GetFeatureCount()):
            feature = shape.GetFeature(x)
            geom = feature.GetGeometryRef()
            # Transform everything... just in case
            geom.Transform(coordTrans)
            jsonobj = feature.ExportToJson(as_object=True)
            jsonLayer['features'].append(jsonobj)

        # print (jsonLayer)

    except GDALException as e:
        print("Failed to read dataset with error {}".format(e))
        raise ParseError('Failed to read uploaded dataset.')

    return jsonLayer


def write_uploaded_file(in_file, destination):
    with open(destination, 'wb') as out_file:
        for chunk in in_file.chunks():
            out_file.write(chunk)

def getEPSG(shape):
    # Load in the projection WKT
    sr = shape.GetSpatialRef()
    # Try to determine the EPSG/SRID code
    res = sr.AutoIdentifyEPSG()
    if res == 0: # success
        print('SRID=' + sr.GetAuthorityCode(None))
    else:
        print('Could not determine SRID')


# Create your views here.
class UploadFile(APIView):
    def post(self, request):
        # This will automatically clean up after us.
        with TemporaryDirectory() as directory:
            file_obj = request.data['file']
            layer = get_layer_from_file(file_obj, directory)

        return Response(layer)
