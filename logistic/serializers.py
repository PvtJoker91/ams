from common_archive.models import ArchiveBox, Dossier
from common_archive.serializers import ABSerializer, ShelfSerializer, DossierSerializer
from services.archive_box import update_box_storage_address, create_box_or_update_status, update_box_status
from services.dossiers import update_dossier_box_and_status


class ABPlacementSerializer(ABSerializer):
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


class DossierCompletionSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('barcode', 'current_sector', 'status', 'archive_box')

    def update(self, instance, validated_data):
        return update_dossier_box_and_status(instance, validated_data)


class ABCompletionSerializer(ABSerializer):
    dossiers = DossierCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def create(self, validated_data):
        return create_box_or_update_status(validated_data)

    def update(self, instance, validated_data):
        return update_box_status(instance, validated_data)
