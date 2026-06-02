from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsSellerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return getattr(obj, 'seller_id', None) == request.user.id
