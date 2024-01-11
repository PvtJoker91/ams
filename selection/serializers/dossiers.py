from rest_framework.exceptions import ParseError

from archive.models import Dossier, Registry
from archive.serializers.nested import DossierSerializer, RegistryShortSerializer
from common.services.validators import validate_dossier_barcode
from dossier_requests.models import DossierTask
from selection.models import SelectionOrder


class DossierSelectingSerializer(DossierSerializer):
    registries = RegistryShortSerializer(many=True)

    class Meta:
        model = Dossier
        fields = 'barcode', 'current_sector', 'status', 'archive_box', 'registries'

    def update(self, instance, validated_data):
        if not validate_dossier_barcode(instance.barcode):
            raise ParseError(f'Wrong barcode format')
        tasks = DossierTask.objects.filter(dossier=instance, task_status='on_selection')
        if not tasks.exists():
            raise ParseError(f'Dossier is not in any task')
        tasks.update(task_status='selected')
        for task in tasks:
            orders = SelectionOrder.objects.filter(tasks=task)
            for order in orders:
                order.selected += 1
                order.save()
        requested_dossiers = Dossier.objects.filter(requests__isnull=False).distinct()
        if Registry.objects.filter(dossiers__in=requested_dossiers, status='creation', type='lr').exists():
            reg = Registry.objects.filter(dossiers__in=requested_dossiers, status='creation', type='lr').first()
        elif Registry.objects.filter(dossiers__in=requested_dossiers, status='sent', type='lr').exists():
            reg = Registry.objects.filter(dossiers__in=requested_dossiers, status='sent', type='lr').first()
            raise ParseError(f'Dossier is already in registry {reg.id} which in status "{reg.status}"')
        else:
            reg = Registry.objects.create(status='creation', type='lr')
        if instance not in reg.dossiers.values():
            reg.dossiers.add(instance)
        return super().update(instance, validated_data)
