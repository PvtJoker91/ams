from archive.models import ArchiveBox
from archive.serializers.nested import ABSerializer, ShelfSerializer


class ABPlacementSerializer(ABSerializer):
    storage_address = ShelfSerializer()

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'status', 'storage_address')
