from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if getattr(request, "user_id", None):
            return True


class IsAnonymousOnlyGetPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if getattr(request, "user_id", None):
            return True
