from rest_framework.serializers import ModelSerializer

from bank_clients.models import Contract
from common_archive.serializers import DossierSerializer


class ContractSerializer(ModelSerializer):
    dossiers = DossierSerializer(many=True)
    class Meta:
        model = Contract
        fields = '__all__'