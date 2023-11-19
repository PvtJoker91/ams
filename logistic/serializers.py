from rest_framework import serializers

from common_archive.models import StorageShelf, ArchiveBox
from logistic.services import update_box_storage_address


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageShelf
        fields = ('shelf_code',)


class ABPlacementSerializer(serializers.ModelSerializer):
    storage_address = ShelfSerializer()

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'status', 'storage_address')

    def update(self, instance, validated_data):
        instance.storage_address = update_box_storage_address(validated_data)
        instance.current_sector = validated_data.get('current_sector', instance.current_sector)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
