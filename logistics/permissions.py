from rest_framework.permissions import IsAuthenticated


class IsInLogisticsGroup(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Logists').exists()
