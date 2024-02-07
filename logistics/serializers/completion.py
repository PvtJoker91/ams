from archive.models import ArchiveBox, Dossier
from archive.serializers.nested import ABSerializer, DossierSerializer
from common.services.archive_box import create_or_update_box
from common.services.dossiers import update_dossier_while_box_checking_and_completion
from common.statuses import DOSSIER_COMPLETION_AVAILABLE_STATUSES, AB_COMPLETION_AVAILABLE_STATUSES


class DossierCompletionSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = (
            'barcode',
            'status',
            'current_sector',
            'archive_box'
        )

    def update(self, instance, validated_data):
        return update_dossier_while_box_checking_and_completion(instance, validated_data, DOSSIER_COMPLETION_AVAILABLE_STATUSES)


class ABCompletionSerializer(ABSerializer):
    dossiers = DossierCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def create(self, validated_data):
        return create_or_update_box(validated_data, AB_COMPLETION_AVAILABLE_STATUSES)
