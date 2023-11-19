from common_archive.models import StorageShelf


def update_box_storage_address(data):
    storage_address = dict(data.get('storage_address'))
    if StorageShelf.objects.filter(shelf_code=storage_address.get('shelf_code')):
        storage_address_instance = StorageShelf.objects.get(shelf_code=storage_address.get('shelf_code'))
    return storage_address_instance
