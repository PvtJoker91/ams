from rest_framework.exceptions import ParseError

from common_archive.models import Dossier, Sector


def update_dossiers_in_box_status(archive_box, status):
    Dossier.objects.filter(archive_box=archive_box).update(status=status)


def update_dossier_box_and_status(instance, validated_data):
    sector = validated_data.get('current_sector', None)
    if instance.current_sector != sector:
        instance.archive_box = None
        # instance.current_sector = Sector.objects.get(id=4)
        instance.status = 'Wrong operation'
        instance.save()
        raise ParseError(
            {
                'dossier_sector_error':
                    f"Dossier should not be on this operation. Dossier current sector is {instance.current_sector}"})
    else:
        instance.archive_box = validated_data.get('archive_box', None)
        instance.status = validated_data.get('status', None)
        instance.save()
        return instance
