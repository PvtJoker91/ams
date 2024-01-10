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
        fields = '__all__'
