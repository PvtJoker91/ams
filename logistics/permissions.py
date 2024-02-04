from rest_framework.permissions import IsAuthenticated

from common.permissions import LOGISTICS_PERMISSION_GROUP


class IsInLogisticsGroup(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=LOGISTICS_PERMISSION_GROUP).exists()
