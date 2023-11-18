from rest_framework import serializers

from common_archive.models import ArchiveBox, Dossier
from common_archive.validators import validate_ab_barcode, validate_dossier_barcode


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = ('contract', 'barcode',)

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_dossier_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class ABSerializer(serializers.ModelSerializer):
    dossiers = DossierSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('id', 'barcode', 'current_sector', 'dossiers', 'status')

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_ab_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs
