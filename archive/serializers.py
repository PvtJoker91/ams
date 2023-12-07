from rest_framework import serializers

from bank_clients.serializers import ContractSerializer
from archive.models import ArchiveBox, Dossier, StorageShelf
from services.validators import validate_ab_barcode, validate_dossier_barcode


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = '__all__'

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_dossier_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class ABSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveBox
        fields = '__all__'

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_ab_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageShelf
        fields = ('shelf_code',)


class DossierSearchSerializer(DossierSerializer):
    contract = ContractSerializer()

    class Meta:
        model = Dossier
        fields = ('id', 'barcode', 'contract', 'status')
