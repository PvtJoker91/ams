from rest_framework.exceptions import ParseError

from archive.models import StorageShelf, ArchiveBox
from common.services.statuses import AB_CHECKING_AVAILABLE_STATUSES, AB_PLACEMENT_AVAILABLE_STATUSES
from common.services.dossiers import update_dossiers_in_box_status_and_sector


def create_or_update_box(validated_data, available_statuses):
    if ArchiveBox.objects.filter(barcode=validated_data.get('barcode')).exists():
        archive_box = ArchiveBox.objects.get(barcode=validated_data.get('barcode'))
        if archive_box.status in available_statuses:
            archive_box.status = validated_data.get('status', None)
            archive_box.storage_address = None
            archive_box.save()
            update_dossiers_in_box_status_and_sector(archive_box)
        else:
            raise ParseError(f"Archive box should not be on this operation. Box current operation is {archive_box.status}")
    else:
        archive_box = ArchiveBox.objects.create(**validated_data)
    return archive_box



def update_box_under_checking(instance, validated_data):
    if instance.status in AB_CHECKING_AVAILABLE_STATUSES:
        instance.status = validated_data.get('status')
        instance.current_sector = validated_data.get('current_sector')
        instance.save()
        update_dossiers_in_box_status_and_sector(instance)
    else:
        raise ParseError(f"Archive box should not be on this operation. Box current operation is {instance.status}")
    return instance


def update_box_under_placement(instance, validated_data):
    if instance.status in AB_PLACEMENT_AVAILABLE_STATUSES:
        storage_address = dict(validated_data.get('storage_address'))
        storage_address_instance = StorageShelf.objects.get(shelf_code=storage_address.get('shelf_code'))
        instance.storage_address = storage_address_instance
        instance.current_sector = validated_data.get('current_sector', instance.current_sector)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        update_dossiers_in_box_status_and_sector(instance)
    else:
        raise ParseError(f"Archive box should not be on this operation. Box current operation is {instance.status}")
    return instance
