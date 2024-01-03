from django.utils import timezone
from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossierTask


class TaskSelectingSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    hours_left = serializers.SerializerMethodField()
    location = serializers.CharField()

    class Meta:
        model = DossierTask
        fields = 'id', 'dossier', 'hours_left', 'location',

    def get_hours_left(self, instance) -> str:
        return (instance.order.deadline - timezone.now()) // 3600
