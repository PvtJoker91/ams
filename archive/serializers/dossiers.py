from rest_framework import serializers

from accounts.serializers.nested import AMSUserShortSerializer
from archive.models import Dossier, DossierScan
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
            'status': entry.status,
            'archive_box': None,
            'user_first_name': entry.history_user.first_name,
            'user_last_name': entry.history_user.last_name,
                 } for entry in history_entries]