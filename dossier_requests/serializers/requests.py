from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
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
    deadline = serializers.SerializerMethodField()
    tasks = TaskShortSerializer(many=True)

    class Meta:
        model = DossierRequest
        fields = '__all__'

    def get_deadline(self, instance) -> str:
        return deadline(instance)


class RequestRetrieveSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    creator = UserShortSerializer()
    closer = UserShortSerializer()
    dossiers = DossierSerializer(many=True)

    class Meta:
        model = DossierRequest
        fields = '__all__'

    def get_deadline(self, instance) -> str:
        return deadline(instance)


class RequestDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierRequest
        fields = 'id',
