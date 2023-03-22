from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuMASuOrReadOnly:
    '''
    Full access to available methods and objects is granted for Authors /
    user-roles of Admin, Moderator / SuperUsers. Others (inc. anonymous) are
    provided w/ read-only access to objects and are able to use safe methods.
    '''

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
        )


class AuthOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
