from rest_framework.serializers import ModelSerializer

from archive.models import Registry, Dossier
from dossier_requests.models import DossierTask, DossierRequest


class RegistrySerializer(ModelSerializer):
    class Meta:
        model = Registry
        fields = '__all__'

    def create(self, validated_data):
        """
        Получаем task.id из query_params. Если реестр на выдачу - проверяем, есть ли неотправеленные реестры по заявке.
        Если на возврат в логистику - просто неотравленные. Добавляем досье в существующий, либо в новый.
        """
        request = self.context['request']
        task_id = request.query_params.get('task_id')
        task = DossierTask.objects.get(id=task_id)
        request = task.request.id
        dossier = Dossier.objects.get(barcode=task.dossier.barcode)
        registry_type = validated_data.get('type')
        if registry_type == 'rc':
            dossiers = DossierRequest.objects.get(id=request).dossiers.values('barcode')
            registries = Registry.objects.filter(status='creation', dossiers__in=dossiers, type='rc')
        elif registry_type == 'rl':
            registries = Registry.objects.filter(status='creation', type='rl')
        if registries.exists():
            instance = registries.first()
        else:
            instance = Registry.objects.create(**validated_data)
        if dossier not in instance.dossiers.values():
            instance.dossiers.add(dossier)
        task.task_status = 'completed'
        task.save()
        dossier.status = 'Added to registry'
        dossier.save()
        return instance

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        dossiers = instance.dossiers.values()
        if status == 'sent_to_requests':
            dossiers.update(status='Sent to requests')
        if status == 'sent_to_customer':
            dossiers.update(status='Sent to customer')
        if status == 'sent_to_logistics':
            dossiers.update(status='Sent to logistics')
        return super().update(instance, validated_data)