from rest_framework import serializers

from common_archive.models import ArchiveBox, Dossier
from common_archive.validators import validate_ab_barcode, validate_dossier_barcode


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
