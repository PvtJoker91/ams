from rest_framework.exceptions import ParseError

from common_archive.models import StorageShelf, ArchiveBox
from services.dossiers import update_dossiers_in_box_status


def create_box_or_update_status(validated_data):
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
            archive_box.save()
            update_dossiers_in_box_status(archive_box, archive_box.status)
    else:
        archive_box = ArchiveBox.objects.create(**validated_data)
    return archive_box


def update_box_status(instance, validated_data):
    instance.status = validated_data.get('status')
    instance.save()
    update_dossiers_in_box_status(instance, instance.status)
    return instance


def update_box_storage_address(validated_data):
    storage_address = dict(validated_data.get('storage_address'))
    if StorageShelf.objects.filter(shelf_code=storage_address.get('shelf_code')):
        storage_address_instance = StorageShelf.objects.get(shelf_code=storage_address.get('shelf_code'))
    return storage_address_instance

# def update_dossiers_in_box_sector(instance, validated_data):
#     dossiers = validated_data.pop('dossiers')
#     keep_dossiers = []
#     for dossier in dossiers:
#         if 'id' in dossier.keys():
#             if Dossier.objects.filter(id=dossier['id']).exists():
#                 d = Dossier.objects.get(id=dossier['id'])
#                 d.sector = dossier.get('sector', d.sector)
#                 d.save()
#                 keep_dossiers.append(d.id)
#             else:
#                 continue
#         else:
#             d = Dossier.objects.create(**dossier, archive_box=instance)
#             keep_dossiers.append(d.id)
#     for dossier in instance.dossiers:
#         if dossier.id not in keep_dossiers:
#             dossier.delete()
#     return instance
