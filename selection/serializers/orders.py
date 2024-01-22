from rest_framework import serializers

from accounts.serializers.nested import AMSUserShortSerializer
from dossier_requests.models import DossierTask
from selection.models import SelectionOrder
from selection.serializers.print import TaskPrintSerializer


class SelectionOrderSerializer(serializers.ModelSerializer):
    tasks = TaskPrintSerializer(many=True)
    creator = AMSUserShortSerializer()
    executor = AMSUserShortSerializer()

    class Meta:
        model = SelectionOrder
        fields = '__all__'


class SelectionOrderCreateSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(queryset=DossierTask.objects.only('id'), many=True)

    class Meta:
        model = SelectionOrder
        fields = 'tasks', 'creator', 'executor'

    def create(self, validated_data):
        tasks = validated_data.get('tasks', [])
        task_ids = [task.id for task in tasks]
        task_instances = DossierTask.objects.filter(id__in=task_ids)
        task_instances.update(task_status='on_selection')
        return super().create(validated_data)
