from rest_framework.permissions import IsAuthenticated

from services.permissions import ORDERS_PERMISSION_GROUP


class IsInOrdersGroup(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=ORDERS_PERMISSION_GROUP).exists()