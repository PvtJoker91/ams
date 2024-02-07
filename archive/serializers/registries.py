from rest_framework import serializers

from archive.models import Registry
from common.services.dossiers import update_dossiers_in_registry
from common.services.registries import add_dossier_to_registry_after_task_execute


class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        task_id = request.query_params.get('task_id')
        return add_dossier_to_registry_after_task_execute(task_id, validated_data)

    def update(self, instance, validated_data):
        reg_status = validated_data.get('status', None)
        reg_type = instance.type
        dossiers = instance.dossiers.values()
        update_dossiers_in_registry(dossiers, reg_status, reg_type)
        return super().update(instance, validated_data)
