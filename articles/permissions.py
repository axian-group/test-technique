from rest_framework import permissions

class IsAdminOrEditorOrReadOnly(permissions.BasePermission):
    """
    Admin: full access
    Editor: CRUD on own articles
    Reader: read-only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name="Editor").exists():
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.author == request.user
        if request.user.groups.filter(name="Reader").exists():
            return request.method in permissions.SAFE_METHODS
        return False
