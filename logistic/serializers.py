from rest_framework import serializers

from common_archive.models import StorageShelf, ArchiveBox


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageShelf
        fields = ('shelf_code',)


class ABPlacementSerializer(serializers.ModelSerializer):
    storage_address = ShelfSerializer(read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'status', 'storage_address')
