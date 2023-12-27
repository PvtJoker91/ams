from archive.models import Dossier
from archive.serializers.nested import DossierSerializer
from bank_clients.serializers.search import ContractSearchSerializer


class DossierSearchSerializer(DossierSerializer):
    contract = ContractSearchSerializer()

    class Meta:
        model = Dossier
        fields = ('barcode', 'contract', 'status')

