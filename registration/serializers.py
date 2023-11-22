
from common_archive.models import ArchiveBox, Dossier
from common_archive.serializers import ABSerializer, DossierSerializer
from services.archive_box import create_box


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
        return create_box(validated_data)
