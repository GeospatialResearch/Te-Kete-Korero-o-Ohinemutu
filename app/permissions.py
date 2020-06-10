from rest_framework import permissions
from .models import Story, StoryBodyElement, StoryGeomAttrib, StoryGeomAttribMedia, CoAuthor, Nest, WhanauGroupInvitation, Sector
# from django.contrib.auth.models import User

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

        if isinstance(obj, Story):
            # CoAuthors can update and delete
            coauths = CoAuthor.objects.filter(story = obj.id).values_list("co_author", flat=True)
            coauths = list(coauths)
            if request.user.id in coauths:
                return True

            return obj.owner == request.user

        # Finally, if the user owns the thing, he can do update and delete.

        if isinstance(obj, StoryBodyElement):
            return obj.story.owner == request.user

        if isinstance(obj, StoryGeomAttrib):
            try:
                storybodyelem = StoryBodyElement.objects.filter(geom_attr=obj)[0]
                coauths = CoAuthor.objects.filter(story = obj.story.id).values_list("co_author", flat=True)
                coauths = list(coauths)
                return storybodyelem.story.owner == request.user or request.user.id in coauths
            except Exception as e:
                return True

        if isinstance(obj, StoryGeomAttribMedia):
            geom_attr = StoryGeomAttrib.objects.filter(id=obj.geom_attr.id)[0]
            try:
                storybodyelem = StoryBodyElement.objects.filter(geom_attr=geom_attr)[0]
                coauths = CoAuthor.objects.filter(story = obj.story.id).values_list("co_author", flat=True)
                coauths = list(coauths)
                return storybodyelem.story.owner == request.user or request.user.id in coauths
            except Exception as e:
                return True

        if isinstance(obj, Nest):
            if obj.created_by == request.user:
                return True
            else:
                whanausector = Sector.objects.get(name='Whānau')
                return (request.user.is_staff and obj.kinship_sector != whanausector)

        if isinstance(obj, WhanauGroupInvitation):
            return obj.invitee == request.user
