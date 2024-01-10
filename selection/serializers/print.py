from rest_framework import serializers

from archive.models import ArchiveBox, Dossier
from archive.serializers.nested import ShelfSerializer
from dossier_requests.models import DossierTask


class ABPrintSerializer(serializers.ModelSerializer):
    storage_address = ShelfSerializer()

    class Meta:
        model = ArchiveBox
        fields = 'barcode', 'storage_address'


class DossierPrintSerializer(serializers.ModelSerializer):
    archive_box = ABPrintSerializer()

    class Meta:
        model = Dossier
        fields = 'barcode', 'archive_box', 'status'


class TaskPrintSerializer(serializers.ModelSerializer):
    dossier = DossierPrintSerializer()

    class Meta:
        model = DossierTask
        fields = 'id', 'dossier', 'task_status'
