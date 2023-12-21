from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossierTask
from orders.serializers.nested import OrderShortSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = '__all__'


class TaskListSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    order = OrderShortSerializer()

    class Meta:
        model = DossierTask
        fields = '__all__'



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