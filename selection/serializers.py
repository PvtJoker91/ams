from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from archive.models import Dossier
from archive.serializers.nested import DossierSerializer, ABSerializer
from archive.statuses import DOSSIER_SELECTING_AVAILABLE_STATUSES
from common.services.dossiers import update_dossier, check_dossier_in_task
from orders.models import DossierTask
from selection.models import SelectionOrder


class DossierSelectingSerializer(DossierSerializer):
    archive_box = ABSerializer()

    class Meta:
        model = Dossier
        fields = ('barcode', 'current_sector', 'status', 'archive_box')

    def update(self, instance, validated_data):
        if not check_dossier_in_task(instance):
            raise ParseError(f"Dossier is not in any task")
        return update_dossier(instance, validated_data, DOSSIER_SELECTING_AVAILABLE_STATUSES)


class TaskSelectingSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    hours_left = serializers.SerializerMethodField()
    location = serializers.CharField()

    class Meta:
        model = DossierTask
        fields = 'dossier', 'hours_left', 'location',

    def get_hours_left(self, instance):
        return (instance.order.deadline - timezone.now()) // 3600



class SelectionOrderSerializer(serializers.ModelSerializer):
    dossiers = DossierSelectingSerializer(many=True)

    class Meta:
        model = SelectionOrder
        fields = '__all__'
