def update_dossiers_in_box_sector(archive_box):
    dossiers = archive_box.dossiers.all()
    for dossier in dossiers:
        dossier.current_sector = archive_box.current_sector
        dossier.status = archive_box.status
        dossier.save()

def update_dossier_box(dossier, archive_box=None):
    dossier.archive_box = archive_box

