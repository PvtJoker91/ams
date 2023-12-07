from archive.models import ArchiveBox, Dossier
from archive.serializers import ABSerializer, DossierSerializer
from services.archive_box import create_or_update_box_under_registration


class DossierRegSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('contract', 'barcode', 'current_sector', 'status', 'archive_box')


class ABRegSerializer(ABSerializer):
    dossiers = DossierRegSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status', 'storage_address',)

    def create(self, validated_data):
        return create_or_update_box_under_registration(validated_data)
