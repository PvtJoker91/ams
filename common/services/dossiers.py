from django.db import transaction

from archive.models import Dossier
from common.services.registries import registry_accepting
from common.validators import validate_dossier_barcode, validate_dossier_status
from dossier_requests.models import DossierTask


def update_dossiers_in_box_status_and_sector(archive_box):
    with transaction.atomic():
        Dossier.objects.filter(archive_box=archive_box).update(
            status=archive_box.status,
            current_sector=archive_box.current_sector)


def update_dossier(instance: Dossier, validated_data: dict, available_statuses: tuple) -> Dossier:
    barcode = validated_data.get('barcode')
    validate_dossier_barcode(barcode)
    validate_dossier_status(instance, available_statuses)
    archive_box = validated_data.get('archive_box', None)
    current_sector = validated_data.get('current_sector', None)
    status = validated_data.get('status', None)
    with transaction.atomic():
        if instance.archive_box != archive_box:
            instance.archive_box = archive_box
        if instance.current_sector != current_sector:
            instance.current_sector = current_sector
        instance.status = status
        instance.save()
        registry_accepting(instance, 'rl')
        return instance


def check_dossier_in_task(instance: Dossier) -> bool:
    return DossierTask.objects.filter(dossier=instance).exists()


def update_dossiers_in_registry(dossiers, reg_status: str, reg_type: str) -> None:
    if reg_status == 'sent' and reg_type == 'lr':
        dossiers.update(status='Sent to requests')
    if reg_status == 'sent' and reg_type == 'rc':
        dossiers.update(status='Sent to customer')
    if reg_status == 'sent' and reg_type == 'rl':
        dossiers.update(status='Sent to logistics')
