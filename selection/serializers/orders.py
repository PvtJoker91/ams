from rest_framework import serializers

from accounts.serializers.nested import AMSUserShortSerializer
from common.services.dossier_tasks import change_tasks_status_while_order_creation
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
        change_tasks_status_while_order_creation(tasks)
        return super().create(validated_data)
