from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from common_archive.models import ArchiveBox, Dossier
from registration.serializers import ABRegSerializer, DossierRegSerializer
from services.validators import validate_dossier_barcode


@extend_schema_view(create=extend_schema(summary='Create/open archive box', tags=['Registration']), )
class ABRegView(ModelViewSet):
    queryset = ArchiveBox.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ABRegSerializer
    lookup_field = 'barcode'
    http_method_names = ('post',)


@extend_schema_view(create=extend_schema(summary='Dossier registration to archive box', tags=['Registration']),
                    list=extend_schema(summary='Get dossiers', tags=['Registration']), )
class DossierRegView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    permission_classes = [AllowAny]
    serializer_class = DossierRegSerializer
    lookup_field = 'barcode'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode',]
    http_method_names = ('get', 'post',)

    def list(self, request, *args, **kwargs):
        barcode = request.GET.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        queryset = self.filter_queryset(self.get_queryset())
        if queryset:
            instance = queryset.first()
            if instance.current_sector.id != 1:
                raise ParseError(
                    {'dossier_sector_error':
                    f"Dossier should not be on this operation. Dossier current sector is {instance.current_sector}"})
            elif instance.archive_box:
                raise ParseError(
                    {'dossier_box_error':
                         f"Dossier is already registred in archive box {instance.archive_box.barcode}"})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
