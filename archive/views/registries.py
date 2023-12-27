from rest_framework.serializers import ModelSerializer

from archive.models import Registry
from archive.serializers.nested import DossierSerializer


class RegistrySerializer(ModelSerializer):
    dossiers = DossierSerializer(many=True)

    class Meta:
        model = Registry
        fields = '__all__',