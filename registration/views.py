from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from archive.models import ArchiveBox, Dossier
from common.statuses import DOSSIER_REGISTRATION_AVAILABLE_STATUSES
from common.validators import validate_dossier_barcode, validate_dossier_status
from registration.permissions import IsInRegistrationGroup
from registration.serializers import ABRegSerializer, DossierRegSerializer


@extend_schema_view(create=extend_schema(summary='Create/open/close archive box', tags=['Registration']),
                    destroy=extend_schema(summary='Delete empty archive box', tags=['Registration']),
                    )
class ABRegView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = ArchiveBox.objects.all()
    permission_classes = [IsInRegistrationGroup]
    serializer_class = ABRegSerializer
    lookup_field = 'barcode'
    http_method_names = ('post', 'delete')

    def get_queryset(self):
        return ArchiveBox.objects.all().select_related('storage_address')


@extend_schema_view(
    create=extend_schema(summary='Dossier registration to archive box', tags=['Registration']),
    list=extend_schema(summary='Get dossiers', tags=['Registration']), )
class DossierRegView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Dossier.objects.all()
    permission_classes = [IsInRegistrationGroup]
    serializer_class = DossierRegSerializer
    lookup_field = 'barcode'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode', ]
    http_method_names = ('get', 'post',)

    def get_queryset(self):
        return Dossier.objects.all()

    def list(self, request, *args, **kwargs):
        barcode = request.GET.get('barcode', None)
        if barcode:
            validate_dossier_barcode(barcode)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset:
            instance = queryset.first()
            validate_dossier_status(instance, DOSSIER_REGISTRATION_AVAILABLE_STATUSES)
            if instance.archive_box:
                raise ParseError(
                    {'dossier_box_error':
                         f"Досье уже зарегистрировано в боксе {instance.archive_box.barcode}"})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
