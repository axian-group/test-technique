from rest_framework import permissions


class ArticlePermission(permissions.BasePermission):
    """
    Custom permission for Article model.
    
    - Admin: Full CRUD on all articles
    - Editor: CRUD on own articles, read-only on others
    - Reader: Read-only access
    """
    
    def has_permission(self, request, view):
        """Check if user has permission to access the view."""
        # Authenticated users can access the view
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin has full access
        if request.user.is_admin:
            return True
        
        # Allow read-only methods for everyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True

        # Writes:
        # - POST: only editors can create
        if request.method == 'POST':
            return request.user.is_editor

        # - PUT/PATCH/DELETE: allow editors to proceed to object-level checks
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user.is_editor

        # Default deny for any other non-safe methods
        return False
    
    def has_object_permission(self, request, view, obj):
        """Check if user has permission to access the specific article."""
        # Admin has full access
        if request.user.is_admin:
            return True
        
        # Everyone can read
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Editor can modify their own articles
        if request.user.is_editor and obj.author == request.user:
            return True
        
        # Reader has no write access
        return False
