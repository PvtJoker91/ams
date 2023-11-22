from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from common_archive.models import ArchiveBox, Dossier
from registration.serializers import ABRegSerializer, DossierRegSerializer


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
    queryset = Dossier.objects.all()
    permission_classes = [AllowAny]
    serializer_class = DossierRegSerializer
    lookup_field = 'barcode'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode',]
    http_method_names = ('get', 'post',)


