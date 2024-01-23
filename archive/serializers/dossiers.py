from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from accounts.serializers.nested import AMSUserShortSerializer
from archive.models import Dossier, DossierScan
from archive.serializers.nested import DossierSerializer, ABSerializer, SectorSerializer
from bank_clients.serializers.search import ContractSearchSerializer


class DossierScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierScan
        fields = '__all__'


class DossierListSerializer(DossierSerializer):
    contract = ContractSearchSerializer()

    class Meta:
        model = Dossier
        fields = ('barcode', 'contract',)


class DossierDetailSerializer(DossierSerializer):
    contract = ContractSearchSerializer()
    archive_box = ABSerializer()
    registerer = AMSUserShortSerializer()
    current_sector = SectorSerializer()
    location = serializers.CharField()
    history = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = ('barcode',
                  'contract',
                  'status',
                  'current_sector',
                  'archive_box',
                  'registerer',
                  'registration_date',
                  'location',
                  'history')

    def get_history(self, obj) -> list:
        history_entries = obj.history.all()

        return [{
            'timestamp': entry.history_date.strftime("%d.%m.%Y %H:%M"),
            'status': entry.history_object.status,
            'archive_box': self.get_archive_box(entry),
            'location': self.get_location(entry),
            'user_first_name': entry.history_user.first_name if entry.history_user else None,
            'user_last_name': entry.history_user.last_name if entry.history_user else None,
        } for entry in history_entries]

    def get_archive_box(self, entry):
        try:
            archive_box = entry.history_object.archive_box
            if archive_box:
                return archive_box.barcode
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_location(self, entry):
        try:
            if self.get_archive_box(entry):
                if entry.history_object.archive_box.storage_address:
                    return entry.history_object.archive_box.storage_address.shelf_code
                else:
                    return None
            else:
                return None
        except ObjectDoesNotExist:
            return None
