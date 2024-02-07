import datetime

from rest_framework import serializers

from common.services.requests import change_request_status
from dossier_requests.models import DossierTask
from dossier_requests.serializers.nested import RequestShortSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'dossier', 'request', 'task_status'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id', 'executor', 'task_status', 'commentary'

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        change_request_status(instance)
        return instance


class TaskListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'

    def get_deadline(self, instance) -> datetime.datetime:
        request = instance.request
        return request.deadline.__format__('%d.%m.%Y %H:%M')


class TaskRetrieveSerializer(serializers.ModelSerializer):
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id',
