from rest_framework import permissions
from .models import StoryBodyElement, StoryGeomAttrib, StoryGeomAttribMedia


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):

        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Anonymous don't get permission to create/update objects
        if request.user.is_anonymous:
            return False

        # Admins do!
        if request.user.is_superuser:
            return True

        return True

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Anonymous don't get access
        if request.user.is_anonymous:
            return False

        # Admins can update and delete
        if request.user.is_superuser:
            return True

        # Finally, if the user owns the thing, he can do update and delete.

        if isinstance(obj, StoryBodyElement):
            return obj.story.owner == request.user

        if isinstance(obj, StoryGeomAttrib):
            try:
                storybodyelem = StoryBodyElement.objects.filter(geom_attr=obj)[0]
                return storybodyelem.story.owner == request.user
            except Exception as e:
                return True

        if isinstance(obj, StoryGeomAttribMedia):
            geom_attr = StoryGeomAttrib.objects.filter(id=obj.geom_attr.id)[0]
            try:
                storybodyelem = StoryBodyElement.objects.filter(geom_attr=geom_attr)[0]
                return storybodyelem.story.owner == request.user
            except Exception as e:
                return True

        # if story
        return obj.owner == request.user
