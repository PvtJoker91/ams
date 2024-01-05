from rest_framework.serializers import ModelSerializer

from archive.models import Registry


class RegistrySelectionSerializer(ModelSerializer):
    class Meta:
        model = Registry
        fields = '__all__'

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if status == 'sent':
            dossiers = instance.dossiers.values()
            dossiers.update(status='Sent to requests')
        return super().update(instance, validated_data)