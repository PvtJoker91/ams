from rest_framework.exceptions import ParseError

from archive.models import Dossier
from archive.statuses import DOSSIER_COMPLETION_AVAILABLE_STATUSES, DOSSIER_CHECKING_AVAILABLE_STATUSES


def update_dossiers_in_box_status_and_sector(archive_box):
    Dossier.objects.filter(archive_box=archive_box).update(status=archive_box.status,
                                                           current_sector=archive_box.current_sector)


def update_dossier_under_completion(instance, validated_data):
    if instance.status not in DOSSIER_COMPLETION_AVAILABLE_STATUSES:
        instance.archive_box = None
        instance.status = 'Wrong operation/sector'
        instance.save()
        raise ParseError(
            {
                'dossier_status_error':
                    f"Dossier should not be on this operation. Dossier current status is {instance.status}"})
    else:
        instance.archive_box = validated_data.get('archive_box', None)
        instance.status = validated_data.get('status', None)
        instance.save()
        return instance


def update_dossier_under_checking(instance, validated_data):
    if instance.status not in DOSSIER_CHECKING_AVAILABLE_STATUSES:
        instance.archive_box = None
        instance.status = 'Wrong operation/sector'
        instance.save()
        raise ParseError(
            {
                'dossier_status_error':
                    f'Dossier should not be on this operation. Dossier current status is {instance.status}'})
    else:
        instance.archive_box = validated_data.get('archive_box', None)
        instance.status = validated_data.get('status', None)
        instance.save()
        return instance
