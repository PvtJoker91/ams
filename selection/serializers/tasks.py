from django.utils import timezone
from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from dossier_requests.models import DossierTask


class TaskSelectingSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    hours_left = serializers.SerializerMethodField()
    location = serializers.CharField()

    class Meta:
        model = DossierTask
        fields = 'id', 'dossier', 'hours_left', 'location',

    def get_hours_left(self, instance) -> str:
        return (instance.request.deadline - timezone.now()) // 3600
