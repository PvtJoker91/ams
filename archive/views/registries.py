from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

from archive.models import Registry
from archive.serializers.registries import RegistrySerializer
from common.pagination import CustomPagination
from dossier_requests.permissions import IsInRequestsGroup

User = get_user_model()
@extend_schema_view(create=extend_schema(summary='Create/add dossier to registry', tags=['Units']),
                    partial_update=extend_schema(summary='Send registry', tags=['Units']),
                    list=extend_schema(summary='Registry list', tags=['Units']),
                    retrieve=extend_schema(summary='Registry detail', tags=['Units']),
                    )
class RegistryView(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    permission_classes = [IsInRequestsGroup]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    http_method_names = ('patch', 'post', 'get')
    filterset_fields = [
        'type',
        'status',
    ]
    ordering_fields = [
        'type',
        'status',
        'time_create',
    ]
    ordering = ['-time_create']

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response

    def get_queryset(self):
        return Registry.objects.all().prefetch_related('dossiers', 'checked_dossiers')

    # def get_queryset(self):
    #     user = self.request.user
    #     if user:
    #         instance = User.objects.get(id=user.id)
    #         if instance.groups.values().filter(name='Managers').exists():
    #             return super().get_queryset()
    #         if instance.groups.values().filter(name='Archive clients').exists():
    #             return Registry.objects.filter(type='rc', status='sent_to_customer')
    #         if instance.groups.values().filter(name='Logistics').exists():
    #             return Registry.objects.filter(Q(type='lr') | Q(Q(type='rl') & Q(status='sent_to_logistics')))
    #         if instance.groups.values().filter(name='Requests').exists():
    #             return Registry.objects.filter(Q(type__in=('rl', 'rc')) | Q(Q(type='lr') & Q(status='sent_to_requests')))
    #     return super().get_queryset()
