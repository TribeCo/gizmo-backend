
from rest_framework.permissions import BasePermission ,SAFE_METHODS

class ArticlePostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.methods in SAFE_METHODS:
            return True
        return request.user == obj.user
