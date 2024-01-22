from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from accounts.serializers.nested import AMSUserShortSerializer
from archive.models import Dossier, DossierScan, ArchiveBox
from archive.serializers.nested import DossierSerializer, ABSerializer
from bank_clients.serializers.search import ContractSearchSerializer


class DossierScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierScan
        fields = '__all__'


class DossierDetailSerializer(DossierSerializer):
    contract = ContractSearchSerializer()
    scans = DossierScanSerializer(many=True)
    archive_box = ABSerializer()
    registerer = AMSUserShortSerializer()
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
                  'scans',
                  'location',
                  'history')

    def get_history(self, obj) -> list:
        history_entries = obj.history.all()

        return [{
            'timestamp': entry.history_date.strftime("%d.%m.%Y %H:%M"),
            'status': entry.history_object.status,
            'archive_box': self.get_archive_box_name(entry),
            'user_first_name': entry.history_user.first_name if entry.history_user else None,
            'user_last_name': entry.history_user.last_name if entry.history_user else None,
            # 'diff': entry.diff_against(entry.prev_record).changed_fields if entry.prev_record else None,
        } for entry in history_entries]

    def get_archive_box_name(self, entry):
        try:
            archive_box = entry.history_object.archive_box
            if archive_box:
                return archive_box.barcode
            else:
                return None
        except ObjectDoesNotExist:
            return None
