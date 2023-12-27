from rest_framework.exceptions import ParseError

from archive.models import Dossier
from orders.models import DossierTask


def update_dossiers_in_box_status_and_sector(archive_box):
    Dossier.objects.filter(archive_box=archive_box).update(status=archive_box.status,
                                                           current_sector=archive_box.current_sector)


def update_dossier(instance, validated_data, available_statuses):
    if instance.status not in available_statuses:
        instance.archive_box = None
        instance.status = 'Wrong operation/sector'
        instance.save()
        raise ParseError(f"Dossier should not be on this operation. Dossier current status is {instance.status}")
    else:
        instance.archive_box = validated_data.get('archive_box', None)
        instance.status = validated_data.get('status', None)
        instance.save()
        return instance


def check_dossier_in_task(instance):
    return DossierTask.objects.filter(dossier=instance.id).exists()

# единая проверка досье на всех операциях -  надо сделать!
def check_dossier(instance, available_statuses):
    if instance.status not in available_statuses:
        instance.archive_box = None
        instance.status = 'Wrong operation/sector'
        instance.save()
        raise ParseError(f"Dossier should not be on this operation. Dossier current status is {instance.status}")
    if check_dossier_in_task(instance):
        # создать реестр для передачи в запросы
        pass
