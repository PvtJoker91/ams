from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossierTask
from orders.serializers.nested import OrderShortSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'dossier', 'order', 'task_status'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id', 'executor', 'task_status', 'commentary'


class TaskListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    dossier = DossierSerializer()
    order = OrderShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'

    def get_deadline(self, instance):
        order = instance.order
        return order.deadline


class TaskRetrieveSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    order = OrderShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = 'id',
