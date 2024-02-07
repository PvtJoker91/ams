from rest_framework import serializers
from rest_framework.exceptions import ParseError

from archive.models import Dossier, Registry
from archive.serializers.nested import DossierSerializer, RegistryShortSerializer
from common.services.dossier_tasks import change_tasks_status_while_dossier_selecting
from common.services.registries import add_dossier_to_registry_while_selecting
from common.validators import validate_dossier_barcode
from dossier_requests.models import DossierTask
from selection.models import SelectionOrder


class DossierSelectingSerializer(DossierSerializer):
    registries = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = 'barcode', 'current_sector', 'status', 'archive_box', 'registries'

    def get_registries(self, instance) -> list:
        registries_instances = instance.registries.filter(status='creation', type='lr')
        return RegistryShortSerializer(registries_instances, many=True).data

    def update(self, instance, validated_data):
        """
        Получаем таски по досье. Меняем статус тасков и добавляем досье в "selected" у наряда. Добавляем досье в
        существующий реестр в статусе "creation", либо в новый.
        """
        validate_dossier_barcode(instance.barcode)
        change_tasks_status_while_dossier_selecting(instance)
        add_dossier_to_registry_while_selecting(instance)
        return super().update(instance, validated_data)
