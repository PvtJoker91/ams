from bank_clients.models import Contract
from common_archive.models import ArchiveBox, Dossier
from common_archive.serializers import ABSerializer, DossierSerializer


class ABRegSerializer(ABSerializer):

    def create(self, validated_data):
        ab, _ = ArchiveBox.objects.update_or_create(
            barcode=validated_data.get('barcode', None),
            defaults={'current_sector': validated_data.get('current_sector', None)})
        return ab


class DossierRegSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('barcode',)

    def create(self, validated_data):
        barcode = validated_data.get('barcode', None)
        if barcode:
            if Contract.objects.filter(barcode=barcode):
                contract = Contract.objects.get(barcode=barcode)
                validated_data['contract'] = contract
        instance = super().create(validated_data)
        return instance
