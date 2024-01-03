from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier
from archive.serializers.dossiers import DossierSearchSerializer
from archive.serializers.nested import DossierSerializer


@extend_schema_view(
    list=extend_schema(summary='Dossiers list', tags=['Units']),
    retrieve=extend_schema(summary='Dossier detail', tags=['Units']),
)
class DossierView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = Dossier.objects.all().select_related('contract')
    serializer_class = DossierSearchSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__last_name',
        'contract__client__name',
        'contract__client__middle_name',
        'contract__client__passport',
        'contract__client__birthday',
        'contract__product__name',

    ]
    search_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__passport',
    ]
    ordering = ('contract__client__last_name', 'contract__product__name',)


@extend_schema_view(
    put=extend_schema(summary='Dossiers list to update', tags=['Units']),
)
class DossiersListUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DossierSerializer

    def get_object(self, barcode):
        try:
            return Dossier.objects.get(barcode=barcode)
        except (Dossier.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_barcodes(self, barcode_list):
        for barcode in barcode_list:
            try:
                Dossier.objects.get(barcode=barcode)
            except (Dossier.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        data = request.data
        barcode_list = [i['barcode'] for i in data]
        self.validate_barcodes(barcode_list)
        instances = []
        for temp_dict in data:
            barcode = temp_dict['barcode']
            archive_box = temp_dict['archive_box']
            status = temp_dict['status']
            obj = self.get_object(barcode)
            obj.archive_box = archive_box
            obj.status = status
            obj.save()
            instances.append(obj)
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)
