from rest_framework import permissions

class IsAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin'
            )
        )

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
