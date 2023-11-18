from common_archive.models import ArchiveBox, Dossier
from common_archive.serializers import ABSerializer, DossierSerializer


class ABRegSerializer(ABSerializer):
    def create(self, validated_data):
        ab, _ = ArchiveBox.objects.update_or_create(
            barcode=validated_data.get('barcode', None),
            defaults={'current_sector': validated_data.get('current_sector', None),
                      'status': validated_data.get('status', None),
                      'storage_address': validated_data.get('storage_address', None),
                      })
        return ab


class DossierRegSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = '__all__'
