from rest_framework.permissions import IsAuthenticated

from common.permissions import REGISTRATION_PERMISSION_GROUP


class IsInRegistrationGroup(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=REGISTRATION_PERMISSION_GROUP).exists()