import datetime

from django.db.models import Count
from rest_framework import serializers

from archive.models import Dossier
from archive.serializers.dossiers import DossierScanCountSerializer
from dossier_requests.models import DossierRequest
from dossier_requests.serializers.nested import UserShortSerializer, TaskShortSerializer
from dossier_requests.serializers.utils import deadline


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        exclude = 'dossiers',


class RequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        fields = 'status', 'dossiers', 'closer', 'close_reason', 'time_create', 'time_close'


class RequestListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    service = serializers.CharField(source='get_service_display')
    urgency = serializers.CharField(source='get_urgency_display')
    deadline = serializers.SerializerMethodField()
    tasks = TaskShortSerializer(many=True)

    class Meta:
        model = DossierRequest
        fields = '__all__'

    def get_deadline(self, instance) -> datetime.datetime:
        return deadline(instance)


class RequestRetrieveSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    service = serializers.CharField(source='get_service_display')
    urgency = serializers.CharField(source='get_urgency_display')
    creator = UserShortSerializer()
    closer = UserShortSerializer()
    dossiers = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    class Meta:
        model = DossierRequest
        fields = '__all__'

    def get_deadline(self, instance) -> datetime.datetime:
        return deadline(instance)

    def get_dossiers(self, instance) -> list:
        dossiers = Dossier.objects.filter(requests=instance).annotate(scan_count=Count('scans'))
        serializer = DossierScanCountSerializer(instance=dossiers, many=True)
        return serializer.data


class RequestDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        fields = 'id',
