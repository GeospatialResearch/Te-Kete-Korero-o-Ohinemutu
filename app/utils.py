import re
import os
import tarfile
from zipfile import ZipFile
from rest_framework.exceptions import ValidationError
from geoserver.catalog import Catalog

shp_exts = ['.shp', ]
csv_exts = ['.csv']
kml_exts = ['.kml']
json_exts = ['.json', '.geojson']
vec_exts = shp_exts + csv_exts + kml_exts + json_exts
cov_exts = ['.tif', '.tiff', '.geotiff', '.geotif', '.asc', '.jpg', '.jpeg', '.png', '.vrt', '.grd']


def layer_type(filename):
    """Finds out if a filename is raster or a vector
    """
    base_name, extension = os.path.splitext(filename)

    if extension.lower() == '.zip':
        zf = ZipFile(filename)
        # ZipFile doesn't support with statement in 2.6, so don't do it
        try:
            for n in zf.namelist():
                b, e = os.path.splitext(n.lower())
                if e in vec_exts or e in cov_exts:
                    extension = e
        finally:
            zf.close()

    if extension.lower() in vec_exts:
        return 'vector'
    elif extension.lower() in cov_exts:
        return 'raster'


def get_catalog():
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')
    cat = Catalog("http://geoserver:8080/geoserver/rest/", gs_user, gs_pass)
    return cat
