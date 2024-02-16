from django.core.cache import cache
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

        box_history_cache_name = 'box_history_cache' + str(obj.barcode)
        box_history_cache = cache.get(box_history_cache_name)

        if box_history_cache:
            box_history = box_history_cache
        else:
            history_entries = obj.history.all()
            box_history = [{
                'timestamp': entry.history_date.strftime("%d.%m.%Y %H:%M"),
                'status': entry.history_object.status,
                'location': entry.history_object.storage_address.shelf_code if entry.history_object.storage_address else None,
                'user_first_name': entry.history_user.first_name if entry.history_user else None,
                'user_last_name': entry.history_user.last_name if entry.history_user else None,
            } for entry in history_entries]
            cache.set(box_history_cache_name, box_history, 1000)

        return box_history
