from django.db.models import F, Count
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from archive.models import ArchiveBox
from archive.serializers.archive_box import ABDetailSerializer


@extend_schema_view(
    retrieve=extend_schema(summary='Archive box detail', tags=['Units']),
)
class ABDetailView(mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = ArchiveBox.objects.all()
    serializer_class = ABDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)
    lookup_field = 'barcode'

    def get_queryset(self):
        return ArchiveBox.objects.select_related(
            'current_sector').annotate(
            location=F('storage_address__shelf_code'),
            dossier_count=Count('dossiers')).all()
