from rest_framework import serializers
from rest_framework.exceptions import ParseError

from archive.models import Dossier, Registry
from archive.serializers.nested import DossierSerializer, RegistryShortSerializer
from common.services.validators import validate_dossier_barcode
from dossier_requests.models import DossierTask
from selection.models import SelectionOrder


class DossierSelectingSerializer(DossierSerializer):
    registries = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = 'barcode', 'current_sector', 'status', 'archive_box', 'registries'

    def get_registries(self, instance):
        registries_instances = instance.registries.filter(status='creation', type='lr')
        return RegistryShortSerializer(registries_instances, many=True).data

    def update(self, instance, validated_data):
        """
        Получаем таски по досье. Меняем статус тасков и добавляем досье в "selected" у наряда. Добавляем досье в
        существующий реестр в статусе "creation", либо в новый.
        """
        validate_dossier_barcode(instance.barcode)
        tasks = DossierTask.objects.filter(dossier=instance, task_status='on_selection')
        if not tasks.exists():
            raise ParseError(f'Dossier is not in any task')
        for task in tasks:
            orders = SelectionOrder.objects.filter(tasks=task)
            for order in orders:
                order.selected.add(task.dossier)
            task.task_status = 'selected'
            task.save()
        if Registry.objects.filter(status='creation', type='lr').exists():
            reg = Registry.objects.get(status='creation', type='lr')
        elif Registry.objects.filter(status='sent', type='lr').exists():
            reg = Registry.objects.get(status='sent', type='lr')
            raise ParseError(f'Dossier is already in registry {reg.id} which in status "{reg.status}"')
        else:
            reg = Registry.objects.create(status='creation', type='lr')
        if instance not in reg.dossiers.values():
            reg.dossiers.add(instance)
        return super().update(instance, validated_data)
