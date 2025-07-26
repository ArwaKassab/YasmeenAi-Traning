from rest_framework import permissions

#هي صلاحية لضبط مين بيقدؤ يقرأ ويعدل المراجهات
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # اي حدا فينه يشوف ويقرا المراجعات
        if request.method in permissions.SAFE_METHODS:
            return True
        # مالك المراجعة فقط يلي فينه يعدلها
        return obj.user == request.user

#صلاحية ان كان ادمن
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


#صلاحية ان كان الادمن او المالك 
class IsAdminOrOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin' or
                obj.user == request.user
            )
        )