import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from archive.models import Dossier
from archive.serializers.dossiers import DossierScanCountSerializer
from common.exeptions import CustomAPIException
from common.permissions import NON_STAFF_GROUP
from dossier_requests.models import DossierRequest
from dossier_requests.serializers.nested import UserShortSerializer, TaskShortSerializer
from dossier_requests.serializers.utils import deadline

User = get_user_model()


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        exclude = 'dossiers',


class RequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        fields = 'status', 'dossiers', 'closer', 'close_reason', 'time_create', 'time_close'

    def update(self, instance, validated_data):
        user_id = CurrentUserDefault()
        user_id = self.context['request'].user.id
        user = User.objects.get(id=user_id)
        status = validated_data.get('status', None)
        if status and status == 'accepted' and user.groups.filter(name__in=NON_STAFF_GROUP).exists():
            raise CustomAPIException('Недостаточно прав!')
        return super().update(instance, validated_data)


class RequestListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    tasks = TaskShortSerializer(many=True)

    class Meta:
        model = DossierRequest
        fields = '__all__'

    def get_deadline(self, instance) -> datetime.datetime:
        return deadline(instance)


class RequestRetrieveSerializer(serializers.ModelSerializer):
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
