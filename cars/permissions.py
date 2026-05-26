from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return getattr(obj, 'seller_id', None) == request.user.id

