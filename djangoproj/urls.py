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

# Construct v1 API routes (it needs rest_framework installed)
router = routers.DefaultRouter()
# router.register(r'datasets', views.DatasetViewSet)

v1 = router.urls + [
    url(r'^upload_file/', views.UploadFileView.as_view()),
    url(r'^datasets', views.dataset_list),
    url(r'^features', views.spatial_features)
]

urlpatterns = [
    # Enable django-admin at admin
    path('admin/', admin.site.urls),

    # Version namespaced API routes
    url('^v1/', include(v1)),
]
