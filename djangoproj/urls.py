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
from django.urls import path, re_path
from django.conf.urls import include, url
from rest_framework import routers
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

from rest_framework_jwt.views import obtain_jwt_token
from rest_auth.registration.views import VerifyEmailView
from django.contrib.auth import views as auth_views

# Construct v1 API routes (it needs rest_framework installed)
router = routers.DefaultRouter()
# router.register(r'datasets', views.DatasetViewSet)
router.register(r'stories', views.StoryViewSet)
router.register(r'mediafiles', views.MediaFileViewSet)
router.register(r'storybodyelements', views.StoryBodyElementViewSet)
router.register(r'atuas', views.AtuaViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'coauthors', views.CoAuthorViewSet)
router.register(r'storytypes', views.StoryTypeViewSet)
router.register(r'contenttypes', views.ContentTypeViewSet)
router.register(r'storygeomsattrib', views.StoryGeomAttribViewSet)
router.register(r'storygeomsattribmedia', views.StoryGeomAttribMediaViewSet)
router.register(r'websitetranslation', views.WebsiteTranslationViewSet)
router.register(r'comments', views.CommentViewSet)
# router.register(r'storygeometries', views.StoryGeometryViewSet)

v1 = router.urls + [
    url(r'^upload_file/', views.UploadFileView.as_view()),
    url(r'^update_being_edited_by/', views.UpdateBeingEditedBy.as_view()),
    url(r'^get_being_edited_by/', views.GetBeingEditedBy.as_view()),
    url(r'^upload_media_file/', views.UploadMediaFileView.as_view()),
    url(r'^delete_unused_media/', views.CleanMediaFilesView.as_view()),
    url(r'^delete_unused_geoms/', views.CleanGeomsView.as_view()),
    url(r'^set_layer_style/', views.SetGeoServerDefaultStyle.as_view()),
    url(r'^get_layer_style/', views.GetGeoServerDefaultStyle.as_view()),
    url(r'^delete_layer/', views.DeleteLayer.as_view()),
    url(r'^rename_layer/', views.RenameLayer.as_view()),
    url(r'^get_layer_bbox/', views.get_layer_bbox),
    url(r'^datasets/', views.DatasetList.as_view()),
    url(r'^check_user/', views.GetUser.as_view()),
    url(r'^check_email/$', views.GetEmail.as_view()),
    url(r'^is_admin/', views.IsAdmin.as_view()),

]

urlpatterns = [
    # Enable django-admin at admin
    path('admin/', admin.site.urls),

    # Version namespaced API routes
    url('^v1/', include(v1)),
    # Redirect to the most current API version
    url(r'^$', RedirectView.as_view(url='/v1/')),
    # Login and logout views for the browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # registration and login with django-rest-auth package
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    # The following is needed due to error Reverse for 'account_email_verification_sent' not found.
    url(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # The following is needed due to error NoReverseMatch: Reverse for 'password_reset_confirm' not found.
    # Note: django-rest-auth relies on django.contrib.auth for password resets, but doesn't include the relevant URLs.
    # Rather than including all of the django.contrib.auth.urls, I only included the ones I needed for password resets. When these are defined, the rest_auth URLs work as expected.
    url(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    url(
        regex=r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)'
              r'/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=auth_views.PasswordResetConfirmView,
        name='password_reset_confirm'
    ),

    # in case of using only rest_framework_jwt without django-rest-auth package
    # url(r'^auth-jwt/', obtain_jwt_token)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
