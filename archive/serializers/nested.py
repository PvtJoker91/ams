from rest_framework import serializers

from archive.models import ArchiveBox, Dossier, StorageShelf
from common.services.validators import validate_ab_barcode, validate_dossier_barcode


class ABSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveBox
        fields = '__all__'

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_ab_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class DossierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dossier
        fields = 'barcode',

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_dossier_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageShelf
        fields = ('shelf_code',)
