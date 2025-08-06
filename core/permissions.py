from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrAuthenticated(BasePermission):
    """
    Custom permission:
    - Allow unrestricted GET, HEAD, OPTIONS (read-only) access.
    - Require authentication for POST, PUT, PATCH, DELETE (write) actions.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
