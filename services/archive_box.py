from rest_framework.exceptions import ParseError

from common_archive.models import StorageShelf, ArchiveBox


def create_box(validated_data):
    if ArchiveBox.objects.filter(barcode=validated_data.get('barcode')):
        archive_box = ArchiveBox.objects.get(barcode=validated_data.get('barcode'))
        if archive_box.current_sector != validated_data.get('current_sector', None):
            raise ParseError(
                {
                    'sector_error':
                    f"Archive box should not be on this operation. Box current sector is {archive_box.current_sector}"})
        else:
            archive_box.status = validated_data.get('status', None)
            archive_box.storage_address = None
    else:
        archive_box = ArchiveBox.objects.create(**validated_data)
    return archive_box


def update_box_storage_address(validated_data):
    storage_address = dict(validated_data.get('storage_address'))
    if StorageShelf.objects.filter(shelf_code=storage_address.get('shelf_code')):
        storage_address_instance = StorageShelf.objects.get(shelf_code=storage_address.get('shelf_code'))
    return storage_address_instance
