from rest_framework import serializers

from common_archive.models import ArchiveBox, Dossier, FileBox
from common_archive.validators import validate_ab_barcode, validate_dossier_barcode, validate_fb_barcode


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = ('contract', 'barcode',)

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_dossier_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class FBSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer(many=True, read_only=True)

    class Meta:
        model = FileBox
        fields = ('barcode', 'dossier')

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_fb_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs


class ABSerializer(serializers.ModelSerializer):
    file_box = FBSerializer(many=True, read_only=True)
    dossier = DossierSerializer(many=True, read_only=True)

    class Meta:
        model = ArchiveBox
        fields = ('barcode', 'current_sector', 'file_box', 'dossier')

    def validate(self, attrs):
        barcode = attrs['barcode']
        if not validate_ab_barcode(barcode):
            raise serializers.ValidationError("Wrong barcode format")
        return attrs

    def create(self, validated_data):
        ab, _ = ArchiveBox.objects.update_or_create(
            barcode=validated_data.get('barcode', None),
            defaults={'current_sector': validated_data.get('current_sector', None)})
        return ab
