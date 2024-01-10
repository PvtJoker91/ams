from rest_framework import serializers

from dossier_requests.serializers.nested import RequestShortSerializer
from dossier_requests.models import DossierTask


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'dossier', 'request', 'task_status'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id', 'executor', 'task_status', 'commentary'


class TaskListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'

    def get_deadline(self, instance) -> str:
        request = instance.request
        return request.deadline


class TaskRetrieveSerializer(serializers.ModelSerializer):
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id',
