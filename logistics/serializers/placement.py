from archive.models import ArchiveBox
from archive.serializers.nested import ABSerializer, ShelfSerializer
from common.services.archive_box import update_box_under_placement


class ABPlacementSerializer(ABSerializer):
    storage_address = ShelfSerializer()

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'status', 'storage_address')

    def update(self, instance, validated_data):
        return update_box_under_placement(instance, validated_data)
