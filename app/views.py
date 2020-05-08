# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import UserSerializer, UserSimpleSerializer, CoAuthorSerializer, DatasetSerializer, StorySerializer, StoryGeomAttribSerializer, StoryBodyElementSerializer, MediaFileSerializer, StoryGeomAttribMediaSerializer, WebsiteTranslationSerializer, AtuaSerializer, StoryTypeSerializer, ContentTypeSerializer, CommentSerializer, ProfileSerializer, SectorSerializer, NestSerializer
from django.http import JsonResponse
from .models import Dataset, Story, CoAuthor, StoryGeomAttrib, StoryBodyElement, MediaFile, StoryGeomAttribMedia, WebsiteTranslation, Atua, StoryType, ContentType, Comment, Profile, Sector, Nest
from django.contrib.auth.models import User
from tempfile import TemporaryDirectory
import zipfile
import os
from osgeo import ogr
from geoserver.catalog import Catalog
from django.db import transaction
import re
from .utils import layer_type, get_catalog, SLDfilterByAttrib
import requests
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files import File
import subprocess
from django.conf import settings
from tempfile import NamedTemporaryFile
from django.core.files.storage import default_storage

# Util Functions
def get_layer_from_file(file_obj, directory, request):
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
            dataset = Dataset.objects.get(name = fname, uploaded_by = request.user)
        except Dataset.DoesNotExist:
            dataset = None
        if dataset:
            raise ValidationError("You've already uploaded a resource named " + fname + ".")
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
def insertDB(layer, request):
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
    dataset = Dataset.objects.create(name=filename, geomtype=geomtypecode, uploaded_by=request.user)
    dataset.save()
    print("######### Created dataset record #########")

    if geomtype == 'raster':
        createGeoserverCoverageLayer(layer, request)
    else:
        createGeoserverShpLayer(layer, request)

    return dataset


def createGeoserverShpLayer(layer, request):
    """Creates a datastore of type Shapefile and a FeatureType layer in GeoServer
    using GeoServer REST API through the Python requests module"""
    cat = get_catalog()
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')

    local_filename = layer['localfilename']
    storename = layer['filename'] + '__' + str(request.user.id)
    filename = layer['filename']
    file_extension = layer['extension']

    if file_extension != '.shp':
        raise ValidationError("Please, upload a zipped shapefile instead of a {} file".format(file_extension))

    with open(local_filename, 'rb') as zip_file:
            r_create_layer = requests.put("http://geoserver:8080/geoserver/rest/workspaces/storyapp/datastores/" + storename + "/file.shp?charset=utf-8",
                auth=(gs_user, gs_pass),
                data=zip_file,
                headers={'content-type': 'application/zip'})
            try:
                r_create_layer.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise ValidationError(e)

            if r_create_layer.status_code == 200 or r_create_layer.status_code == 201:
                print("######### Published Geoserver shp datastore and layer #########")

                r_rename_layer = requests.post("http://geoserver:8080/geoserver/rest/workspaces/storyapp/datastores/" + storename + "/featuretypes",
                    auth=(gs_user, gs_pass),
                    data="<featureType><name>" + storename + "</name><nativeName>" + filename + "</nativeName></featureType>",
                    headers={'Content-type': 'text/xml'})
                try:
                    r_rename_layer.raise_for_status()

                except requests.exceptions.HTTPError as e:
                    raise ValidationError(e)

                if r_rename_layer.status_code == 200 or r_rename_layer.status_code == 201:
                    print("######### Geoserver layer renamed #########")
                    # delete layer generated before the layer rename
                    delete_layer({'gs_layername': filename, 'storename': storename})

            cat.reload()
            resource = cat.get_resource(storename)
            if resource.projection is None:
                delete_layer({'gs_layername': storename}, True)
                raise ValidationError("The dataset does not have a defined projection. Please insert a valid dataset.")


def createGeoserverCoverageLayer(layer, request):
    """Creates a datastore of type GeoTIFF and a Coverage layer in GeoServer
    using GeoServer REST API through gsconfig.py"""
    cat = get_catalog()
    filename = layer['filename'] + '__' + str(request.user.id)
    resource = cat.get_resource(filename)

    file_extension = layer['extension']

    if file_extension != '.tif':
        raise ValidationError("Please, upload a raster dataset with .tif instead of a {} file".format(file_extension))

    try:
        if resource is not None:
            cat.create_coveragestore(filename, layer['localfilename'])
        else:
            cat.create_coveragestore(filename, layer['localfilename'], overwrite=True)
        print("######### Created Geoserver coverage #########")

    except Exception as e:
        if str(e) == 'Could not aquire reader for coverage.':
            raise ValidationError(str(e) + " Please, convert your raster file into .tif format.")
        else:
            raise ValidationError(e)

    cat.reload()
    resource = cat.get_resource(filename)
    if resource.projection is None:
        delete_layer({'gs_layername': filename}, True)
        raise ValidationError("The dataset does not have a defined projection. Please insert a valid dataset.")


@transaction.atomic
def update_editor(editor_id, story_id, action):
    story = Story.objects.get(pk = story_id)
    if editor_id is not None:
        editor = User.objects.get(pk = editor_id)

    if action == 'set':
        story.being_edited_by = editor
        story.save()
    else:
        story.being_edited_by = None
        story.save()



@transaction.atomic
def delete_layer(obj, deleteStore=False):

    if deleteStore:
        storename = obj['gs_layername']
    else:
        gs_layername = obj['gs_layername']
        storename = obj['storename']

    cat = get_catalog()
    store = cat.get_store(storename)

    if store.type == 'Shapefile' or store.type == 'PostGIS':
        storetype = 'datastores'
    elif store.type == 'GeoTIFF':
        storetype = 'coveragestores'

    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')

    if deleteStore:
        # Remove from database
        if 'layerid' in obj:
            dataset = Dataset.objects.get(id=obj['layerid']).delete()

        # Remove store and layer from GeoServer
        r_detele = requests.delete("http://geoserver:8080/geoserver/rest/workspaces/storyapp/" + storetype + "/" + storename + "?recurse=true",
            auth=(gs_user, gs_pass))
        try:
            r_detele.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValidationError(e)

        cat.reload()
        style = cat.get_style("style_" + storename)
        if style is not None:
            cat.delete(style)

    else:
        # Remove duplicated layer and featuretype generated before layer rename (first the layer then the feature type)
        r_detele_layer = requests.delete("http://geoserver:8080/geoserver/rest/layers/storyapp:" + gs_layername + ".xml",
            auth=(gs_user, gs_pass))
        r_detele_featuretype = requests.delete("http://geoserver:8080/geoserver/rest/workspaces/storyapp/" + storetype + "/" + storename + "/featuretypes/" + gs_layername + ".xml",
            auth=(gs_user, gs_pass))
        try:
            r_detele_layer.raise_for_status()
            r_detele_featuretype.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValidationError(e)


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
        styleObj = request.data['styleObj']

        dataset = Dataset.objects.get(id=styleObj['layerid'])
        del styleObj['layername']
        del styleObj['layerid']
        dataset.style = styleObj
        dataset.save()

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
            layer = get_layer_from_file(file_obj, directory, request)

            if layer is not None:
                dataset = insertDB(layer, request)

        layer["id"] = dataset.id
        return Response(layer)



def compress_image(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=70)
    new_image = File(im_io, name=image.name)
    return new_image

def compress_video(mediafile,filename,ext):
    # Reduce file size in case of video and audio
    temp_file = NamedTemporaryFile(suffix = ext.lower())
    temp_file_path = temp_file.name
    with open(temp_file_path, 'wb+') as destination:
        for chunk in mediafile.chunks():
            destination.write(chunk)

    outfile = settings.MEDIA_ROOT+"/compressed_"+filename
    subprocess.call(["ffmpeg", "-i", temp_file_path, "-strict", "-2", "-b:v", "300K", outfile])#-b:v 300K
    file_compressed = File(open(outfile, 'rb'))
    file_compressed.name = file_compressed.name.split('compressed_')[1]
    default_storage.delete(outfile)
    return file_compressed


# https://www.techiediaries.com/django-rest-image-file-upload-tutorial/
class UploadMediaFileView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = MediaFileSerializer(data=request.data)

        # Make some validation on media file format
        img_exts = ['.jpg', '.jpeg', '.png', '.svg', '.bmp']
        video_exts = ['.mp4', '.mov']
        audio_exts = ['.mp3']
        filename = str(request.data['file'])
        base_name, ext = os.path.splitext(filename)

        if ext.lower() not in img_exts and ext.lower() not in video_exts and ext.lower() not in audio_exts:
            raise ValidationError("The format of the media file " + filename + " is not supported. Please, upload a media file with one of the following extensions: " + ",".join(img_exts) + "," + ",".join(video_exts) + " and" + ",".join(audio_exts))
        if not re.match("^[a-zA-Z0-9_-]*$", base_name):
            raise ValidationError("The media file name " + base_name + " is invalid. Make sure the name does not have any spaces or special characters.")
        if base_name[0].isdigit():
            raise ValidationError("The media file name can't start with a digit. Please make sure the name starts with an alpha character.")

        if ext.lower() in img_exts:
            request.data['file'] = compress_image(request.data['file'])
        # if ext.lower() in video_exts or ext.lower() in audio_exts:
        #     request.data['file'] = compress_video(request.data['file'],filename,ext)

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

    def get_queryset(self):
        return self.queryset.for_user(self.request.user).order_by('-created_date')

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
    def perform_update(self,serializer):
        serializer.save(being_edited_by = None)


class StoryBodyElementViewSet(viewsets.ModelViewSet):
    serializer_class = StoryBodyElementSerializer
    queryset = StoryBodyElement.objects.all()

    def get_queryset(self):

        # If required, filter for the geom
        geomattr = self.request.query_params.get('geomattr', None)
        if geomattr is not None:
            queryset = self.queryset.filter(geom_attr=geomattr)
            return queryset

        return self.queryset.for_user(self.request.user)


class AtuaViewSet(viewsets.ModelViewSet):
    serializer_class = AtuaSerializer
    queryset = Atua.objects.all()

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class StoryTypeViewSet(viewsets.ModelViewSet):
    serializer_class = StoryTypeSerializer
    queryset = StoryType.objects.all()

class CoAuthorViewSet(viewsets.ModelViewSet):
    serializer_class = CoAuthorSerializer
    queryset = CoAuthor.objects.all()

    def perform_update(self,serializer):
        serializer.save()

class ContentTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()


class StoryGeomAttribViewSet(viewsets.ModelViewSet):
    serializer_class = StoryGeomAttribSerializer
    queryset = StoryGeomAttrib.objects.all()

    def perform_create(self,serializer):
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

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-date')

    @transaction.atomic
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class SectorViewSet(viewsets.ModelViewSet):
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()


class NestViewSet(viewsets.ModelViewSet):
    serializer_class = NestSerializer
    queryset = Nest.objects.all()

    def get_queryset(self):
        queryset_for_user = self.queryset.for_user(self.request.user)
        if queryset_for_user is not None:
            return queryset_for_user.order_by('id')
        return

    def perform_update(self,serializer):
        serializer.save()



### I had to turn the following method into an APIView in order to the request.user don't be AnonymousUser
# def dataset_list(request):
#     if request.method == 'GET':
#         datasets = Dataset.objects.for_user(request.user).values('name', 'geomtype', 'copyright_text', 'assigned_name', 'uploaded_by')
#
#         datasets_list = list(datasets)
#         return JsonResponse(datasets_list, safe=False)

class DatasetList(APIView):
    def get(self, request):
        datasets = Dataset.objects.for_user(request.user).values('id', 'name', 'geomtype', 'copyright_text', 'assigned_name', 'uploaded_by', 'uploaded_by__username', 'shared_with')
        datasets_list = list(datasets)
        return JsonResponse(datasets_list, safe=False)


class UpdateBeingEditedBy(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        story_id = request.data['story_id']
        action = request.data["action"]

        if action == 'set':
            editor = request.data["editor"]
        else:
            editor = None

        update_editor(editor, story_id, action)

        return Response({'result': "ok"})

class GetBeingEditedBy(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        story_id = request.data['story_id']
        story = Story.objects.get(id=story_id)
        return Response({'result': "ok",'being_edited_by':story.being_edited_by.id if story and story.being_edited_by else None})


class DeleteLayer(APIView):
    def post(self, request):

        delete_layer(request.data, True)

        return Response({'result': None})

class AddCopyright(APIView):
    def post(self, request):
        layerid = request.data['layerid']
        copyright_text = request.data['copyrightText']

        if layerid is not None and copyright_text is not None:
            dataset = Dataset.objects.get(id=layerid)
            dataset.copyright_text = copyright_text
            dataset.save()

        return Response({'result': None})

class RenameLayer(APIView):
    def post(self, request):
        layerid = request.data['layerid']
        assignedname = request.data['assignedName']

        if layerid is not None and assignedname is not None:
            dataset = Dataset.objects.get(id=layerid)
            dataset.assigned_name = assignedname
            dataset.save()

        return Response({'result': None})


class SetLayerSharedWith(APIView):
    def post(self, request):
        layerid = request.data['layerid']
        sharedwith = request.data['shared_with']

        if layerid is not None and sharedwith is not None:
            dataset = Dataset.objects.get(id=layerid)
            dataset.shared_with = sharedwith
            dataset.save()

        return Response({'result': None})


def get_layer_bbox(request):
    layername = request.GET.get('layername', None)
    cat = get_catalog()
    if layername is not None:
        resource = cat.get_resource(layername)

    return JsonResponse({'bbox': resource.latlon_bbox})


class GetAllUsers(APIView):
    def get(self, request):
        if request.user is not None and not request.user.is_anonymous:

            if request.user.is_superuser:
                allusers = User.objects.all()
                users_serializer = UserSerializer(allusers, many=True)
            else:
                allusers = User.objects.values('id', 'username')
                users_serializer = UserSimpleSerializer(allusers, many=True)

            return Response({'users': users_serializer.data})
        else:
            return Response({})


class GetUser(APIView):
    def get(self, request):
        if request.user is not None and not request.user.is_anonymous:
            profile_serializer = ProfileSerializer(request.user.profile)
            return Response({'user': {'email': request.user.email, 'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'pk' : request.user.pk, 'profile': profile_serializer.data}})
        else:
            return Response({})


class GetEmail(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if email is not None:
            users = User.objects.all().values_list('email', flat=True)
            if email in users:
                return Response({'emailExists': True})
            else:
                return Response({'emailExists': False})


class IsAdmin(APIView):
    def get(self, request):
        isAdmin = request.user is not None \
            and not request.user.is_anonymous\
            and request.user.is_superuser

        return Response({'isAdmin': isAdmin})


class GetAllProfiles(APIView):
    def get(self, request):
        if request.user.is_superuser:
            profiles = Profile.objects.all()
            profile_serializer = ProfileSerializer(profiles, many=True)

            return Response (profile_serializer.data)

        return Response({})


class ChangeAvatar(APIView):
    def post(self, request):
        imageurl = request.data['imageurl']
        user = request.user

        import base64
        from django.core.files.base import ContentFile
        format, imgstr = imageurl.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='avatar.' + ext)

        user.profile.avatar = data
        user.save()

        profile_serializer = ProfileSerializer(request.user.profile)

        return Response({'avatar': profile_serializer.data['avatar']})


class SaveProfile(APIView):
    def post(self, request):
        inputs = request.data['inputs']
        user = request.user

        if inputs['first_name'] is not '':
            user.first_name = inputs['first_name']
        if inputs['last_name'] is not '':
            user.last_name = inputs['last_name']
        if inputs['pepeha'] is not '':
            user.profile.pepeha = inputs['pepeha']
        if inputs['bio'] is not '':
            user.profile.bio = inputs['bio']
        if inputs['date_birth'] is not '':
            user.profile.birth_date = inputs['date_birth']

        user.save()

        profile_serializer = ProfileSerializer(request.user.profile)

        return Response({'user': {'email': request.user.email, 'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'pk' : request.user.pk, 'profile': profile_serializer.data}})


class SaveAffiliation(APIView):
    def post(self, request):
        userid = request.data['user']
        affiliation = request.data['affiliation']

        user = User.objects.get(pk=userid)

        user.profile.affiliation.clear()
        for nest_id in affiliation:
            user.profile.affiliation.add(nest_id)


        return Response({'user': 'ok' })
