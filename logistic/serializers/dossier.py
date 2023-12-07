from archive.models import Dossier
from archive.serializers import DossierSerializer
from services.dossiers import update_dossier_under_completion, update_dossier_under_checking


class DossierCompletionSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('barcode', 'current_sector', 'status', 'archive_box')

    def update(self, instance, validated_data):
        return update_dossier_under_completion(instance, validated_data)


class DossierCheckSerializer(DossierSerializer):
    class Meta:
        model = Dossier
        fields = ('barcode', 'current_sector', 'status', 'archive_box')

    def update(self, instance, validated_data):
        return update_dossier_under_checking(instance, validated_data)
