from archive.models import ArchiveBox, Dossier
from archive.serializers.nested import ABSerializer, DossierSerializer
from common.services.archive_box import update_box_under_checking
from common.services.dossiers import update_dossier_while_box_checking_and_completion
from common.statuses import DOSSIER_CHECKING_AVAILABLE_STATUSES


class DossierCheckSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = (
            'barcode',
            'status',
            'current_sector',
            'archive_box',
        )

    def update(self, instance, validated_data):
        return update_dossier_while_box_checking_and_completion(instance, validated_data, DOSSIER_CHECKING_AVAILABLE_STATUSES)


class ABCheckSerializer(ABSerializer):
    dossiers = DossierCheckSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def update(self, instance, validated_data):
        return update_box_under_checking(instance, validated_data)
