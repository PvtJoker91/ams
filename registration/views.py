from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bank_clients.models import Contract
from bank_clients.serializers import ContractSerializer
from archive.models import ArchiveBox, Dossier
from archive.statuses import DOSSIER_REGISTRATION_AVAILABLE_STATUSES
from registration.serializers import ABRegSerializer, DossierRegSerializer
from services.validators import validate_dossier_barcode


@extend_schema_view(create=extend_schema(summary='Create/open/close archive box', tags=['Registration']),
                    destroy=extend_schema(summary='Delete empty archive box', tags=['Registration']),
                    )
class ABRegView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = ArchiveBox.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ABRegSerializer
    lookup_field = 'barcode'
    http_method_names = ('post', 'delete')


@extend_schema_view(
    create=extend_schema(summary='Dossier registration to archive box', tags=['Registration']),
    list=extend_schema(summary='Get dossiers', tags=['Registration']), )
class DossierRegView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    permission_classes = [AllowAny]
    serializer_class = DossierRegSerializer
    lookup_field = 'barcode'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode', ]
    http_method_names = ('get', 'post',)

    def list(self, request, *args, **kwargs):
        barcode = request.GET.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        queryset = self.filter_queryset(self.get_queryset())
        if queryset:
            instance = queryset.first()
            if instance.status not in DOSSIER_REGISTRATION_AVAILABLE_STATUSES:
                raise ParseError(
                    {'dossier_status_error':
                         f"Dossier should not be on this operation. Dossier current status is {instance.status}"})
            elif instance.archive_box:
                raise ParseError(
                    {'dossier_box_error':
                         f"Dossier is already registred in archive box {instance.archive_box.barcode}"})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(list=extend_schema(summary='Contracts search', tags=['Registration']), )
class ContractSearchView(mixins.ListModelMixin, GenericViewSet):
    queryset = Contract.objects.all().select_related('product').select_related('client')
    serializer_class = ContractSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                        'contract_number']
    search_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                     'contract_number']
