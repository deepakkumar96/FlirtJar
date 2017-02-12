from rest_framework.permissions import BasePermission


class AllowOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        # Allow get requests for all
        if request.method == 'GET':
            return True
        else:
            return request.user == obj


class AllowOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsInstagramUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_instagram_activated

