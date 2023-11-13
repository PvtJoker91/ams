from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from registration.serializers import ABRegSerializer, DossierRegSerializer


@extend_schema_view(create=extend_schema(summary='Создать/открыть бокс', tags=['Регистрация']), )
class ABRegView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ABRegSerializer
    lookup_field = 'barcode'
    http_method_names = ('post',)


@extend_schema_view(create=extend_schema(summary='Регистрация', tags=['Регистрация']), )
class DossierRegView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DossierRegSerializer
    lookup_field = 'barcode'
    http_method_names = ('post',)
