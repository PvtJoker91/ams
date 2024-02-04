import datetime

from rest_framework import serializers

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
        status = validated_data.get('task_status', instance.task_status)
        executor = validated_data.get('executor', instance.executor)
        commentary = validated_data.get('commentary', instance.commentary)
        instance.task_status = status
        instance.executor = executor
        instance.commentary = commentary
        instance.save()
        request = instance.request
        uncomplete_tasks = request.tasks.filter(task_status__in=('accepted', 'on_selection', 'selected'))
        if not uncomplete_tasks.exists():
            request.status = 'complete'
            request.save()
        else:
            if request.status != 'in_progress':
                request.status = 'in_progress'
                request.save()
        return instance


class TaskListSerializer(serializers.ModelSerializer):
    task_status = serializers.CharField(source='get_task_status_display')
    deadline = serializers.SerializerMethodField()
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'

    def get_deadline(self, instance) -> datetime.datetime:
        request = instance.request
        return request.deadline.__format__('%d.%m.%Y %H:%M')


class TaskRetrieveSerializer(serializers.ModelSerializer):
    task_status = serializers.CharField(source='get_task_status_display')
    request = RequestShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id',
