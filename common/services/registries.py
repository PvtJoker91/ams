
from archive.models import Registry


def registry_accepting(dossier, reg_type):
    registries = Registry.objects.filter(status__in=('sent', 'on_acceptance'), dossiers=dossier, type=reg_type)

    if registries.exists():
        for registry in registries:
            if registry.status == 'sent':
                registry.status = 'on_acceptance'
                registry.save()
            registry.checked_dossiers.add(dossier)

            if list(registry.dossiers.values()) == list(registry.checked_dossiers.values()):
                registry.status = 'accepted'
                registry.save()