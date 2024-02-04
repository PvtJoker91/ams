from rest_framework import serializers

from archive.models import ArchiveBox, Dossier, StorageShelf, Registry, Sector
from common.validators import validate_ab_barcode, validate_dossier_barcode


class ABSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveBox
        fields = 'barcode',

    def validate(self, attrs):
        barcode = attrs['barcode']
        validate_ab_barcode(barcode)
        return attrs


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = 'barcode',

    def validate(self, attrs):
        barcode = attrs['barcode']
        validate_dossier_barcode(barcode)
        return attrs


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageShelf
        fields = 'shelf_code',


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = 'name',


class RegistryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = '__all__'
