from rest_framework import serializers

from archive.models import Dossier, DossierScan
from archive.serializers.nested import DossierSerializer
from bank_clients.serializers.search import ContractSearchSerializer


class DossierScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierScan
        fields = '__all__'


class DossierSearchSerializer(DossierSerializer):
    contract = ContractSearchSerializer()
    scans = DossierScanSerializer(many=True)

    class Meta:
        model = Dossier
        fields = ('barcode', 'contract', 'status', 'scans')
