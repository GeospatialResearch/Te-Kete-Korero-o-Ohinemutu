"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from app import views
from django.conf.urls.static import static
from django.conf import settings

# Construct v1 API routes (it needs rest_framework installed)
router = routers.DefaultRouter()
# router.register(r'datasets', views.DatasetViewSet)
router.register(r'stories', views.StoryViewSet)
router.register(r'mediafiles', views.MediaFileViewSet)
router.register(r'storybodyelements', views.StoryBodyElementViewSet)
router.register(r'storygeomsattrib', views.StoryGeomAttribViewSet)
router.register(r'storygeomsattribmedia', views.StoryGeomAttribMediaViewSet)

v1 = router.urls + [
    url(r'^upload_file/', views.UploadFileView.as_view()),
    url(r'^upload_media_file/', views.UploadMediaFileView.as_view()),
    url(r'^delete_unused_media/', views.CleanMediaFilesView.as_view()),
    url(r'^delete_unused_geoms/', views.CleanGeomsView.as_view()),
    url(r'^set_layer_style/', views.SetGeoServerDefaultStyle.as_view()),
    url(r'^get_layer_style/', views.GetGeoServerDefaultStyle.as_view()),
    url(r'^delete_layer/', views.DeleteLayer.as_view()),
    url(r'^rename_layer/', views.RenameLayer.as_view()),
    url(r'^get_layer_bbox/', views.get_layer_bbox),
    url(r'^datasets/', views.dataset_list),

]

urlpatterns = [
    # Enable django-admin at admin
    path('admin/', admin.site.urls),

    # Version namespaced API routes
    url('^v1/', include(v1)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
