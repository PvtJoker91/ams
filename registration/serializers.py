from archive.models import ArchiveBox, Dossier
from archive.serializers.nested import ABSerializer, DossierSerializer
from common.services.statuses import AB_REGISTRATION_AVAILABLE_STATUSES
from common.services.archive_box import create_or_update_box


class DossierRegSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('contract', 'barcode', 'current_sector', 'status', 'archive_box', 'registerer')


class ABRegSerializer(ABSerializer):
    dossiers = DossierRegSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address')

    def create(self, validated_data):
        return create_or_update_box(validated_data, AB_REGISTRATION_AVAILABLE_STATUSES)
