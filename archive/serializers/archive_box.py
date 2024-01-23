from rest_framework import serializers

from archive.models import Dossier
from archive.serializers.nested import ABSerializer, SectorSerializer


class ABDetailSerializer(ABSerializer):
    dossier_count = serializers.CharField()
    current_sector = SectorSerializer()
    location = serializers.CharField()
    history = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = ('barcode',
                  'status',
                  'current_sector',
                  'dossier_count',
                  'location',
                  'history')

    def get_history(self, obj) -> list:
        history_entries = obj.history.all()

        return [{
            'timestamp': entry.history_date.strftime("%d.%m.%Y %H:%M"),
            'status': entry.history_object.status,
            'location': entry.history_object.storage_address.shelf_code if entry.history_object.storage_address else None,
            'user_first_name': entry.history_user.first_name if entry.history_user else None,
            'user_last_name': entry.history_user.last_name if entry.history_user else None,
        } for entry in history_entries]
