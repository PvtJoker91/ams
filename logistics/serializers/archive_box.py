from archive.models import ArchiveBox
from archive.serializers.nested import ABSerializer, ShelfSerializer
from logistics.serializers.dossier import DossierCompletionSerializer, DossierCheckSerializer
from common.services.archive_box import update_box_under_placement, create_or_update_box_under_completion, \
    update_box_under_checking


class ABPlacementSerializer(ABSerializer):
    storage_address = ShelfSerializer()

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'status', 'storage_address')

    def update(self, instance, validated_data):
        return update_box_under_placement(instance, validated_data)


class ABCheckSerializer(ABSerializer):
    dossiers = DossierCheckSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def update(self, instance, validated_data):
        return update_box_under_checking(instance, validated_data)


class ABCompletionSerializer(ABSerializer):
    dossiers = DossierCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def create(self, validated_data):
        return create_or_update_box_under_completion(validated_data)
