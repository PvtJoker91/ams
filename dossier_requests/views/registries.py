from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import Registry
from archive.serializers.registries import RegistrySerializer
from dossier_requests.permissions import IsInRequestsGroup


@extend_schema_view(create=extend_schema(summary='Create/add dossier to registry', tags=['Requests']),
                    partial_update=extend_schema(summary='Send registry', tags=['Requests']), )
class RegistryRequestsView(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    permission_classes = [IsInRequestsGroup]
    http_method_names = ('patch', 'post',)
