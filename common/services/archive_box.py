from rest_framework.exceptions import ParseError

from archive.models import ArchiveBox
from common.services.dossiers import update_dossiers_in_box_status_and_sector
from common.statuses import AB_CHECKING_AVAILABLE_STATUSES


def create_or_update_box(validated_data: dict, available_statuses: tuple) -> ArchiveBox:
    if ArchiveBox.objects.filter(barcode=validated_data.get('barcode')).exists():
        archive_box = ArchiveBox.objects.get(barcode=validated_data.get('barcode'))
        if archive_box.status in available_statuses:
            archive_box.status = validated_data.get('status', None)
            archive_box.storage_address = None
            archive_box.save()
            update_dossiers_in_box_status_and_sector(archive_box)
        else:
            raise ParseError(
                f"Archive box should not be on this operation. Box current operation is {archive_box.status}")
    else:
        archive_box = ArchiveBox.objects.create(**validated_data)
    return archive_box


def update_box_under_checking(instance: ArchiveBox, validated_data: dict) -> ArchiveBox:
    if instance.status in AB_CHECKING_AVAILABLE_STATUSES:
        instance.status = validated_data.get('status')
        instance.current_sector = validated_data.get('current_sector')
        instance.save()
        if instance.status == 'Checked with an error':
            instance.dossiers.filter(status='Under checking').update(status='Not found while checking',
                                                                     archive_box=None)
        instance.dossiers.all().update(status=instance.status,
                                       current_sector=instance.current_sector)
    else:
        raise ParseError(f"Archive box should not be on this operation. Box current operation is {instance.status}")
    return instance
