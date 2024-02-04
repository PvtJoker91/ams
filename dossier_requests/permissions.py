from rest_framework.permissions import IsAuthenticated

from common.permissions import REQUESTS_PERMISSION_GROUP


class IsInRequestsGroup(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=REQUESTS_PERMISSION_GROUP).exists()