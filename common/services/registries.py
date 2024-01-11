from archive.models import Registry


def registry_accepting(reg_type, dossier):
    registries = Registry.objects.filter(dossiers=dossier, type=reg_type)
    if registries.exists():
        registry = registries.first()
        if registry.status in ('sent_to_requests', 'sent_to_logistics', 'sent_to_client'):
            registry.status = 'on_acceptance'
            registry.save()
        registry.checked_dossiers.add(dossier)
        if list(registry.dossiers.values()) == list(registry.checked_dossiers.values()):
            registry.status = 'accepted'
            registry.save()