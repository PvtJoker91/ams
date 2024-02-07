from rest_framework.exceptions import ParseError

from archive.models import Registry, Dossier
from dossier_requests.models import DossierTask, DossierRequest


def registry_accepting(instance: Dossier, reg_type: str) -> None:
    registries = Registry.objects.filter(status__in=('sent', 'on_acceptance'), dossiers=instance, type=reg_type)

    if registries.exists():
        for registry in registries:
            if registry.status == 'sent':
                registry.status = 'on_acceptance'
                registry.save()
            registry.checked_dossiers.add(instance)

            if list(registry.dossiers.values()) == list(registry.checked_dossiers.values()):
                registry.status = 'accepted'
                registry.save()


def add_dossier_to_registry_while_selecting(instance: Dossier) -> None:
    """ Добавляем досье в существующий реестр в статусе "creation", либо создаём новый и добавляем. """

    if Registry.objects.filter(status='creation', type='lr').exists():
        reg = Registry.objects.get(status='creation', type='lr')
    elif Registry.objects.filter(status='sent', type='lr', dossiers=instance).exists():
        reg = Registry.objects.filter(status='sent', type='lr', dossiers=instance).first()
        raise ParseError(f'Dossier is already in registry {reg.id} which in status "{reg.status}"')
    else:
        reg = Registry.objects.create(status='creation', type='lr')
    if instance not in reg.dossiers.values():
        reg.dossiers.add(instance)


def add_dossier_to_registry_after_task_execute(task_id: int, validated_data: dict) -> Registry:
    """ Получаем таск и его досье. Если реестр на выдачу - проверяем, есть ли неотправеленные реестры по заявке из
    таска. Если на возврат в логистику - просто неотравленные. Добавляем досье в существующий, либо в новый. """
    task = DossierTask.objects.get(id=task_id)
    request = task.request.id
    dossier = Dossier.objects.get(barcode=task.dossier.barcode)
    registry_type = validated_data.get('type')
    registries = []
    if registry_type == 'rc':
        dossiers = DossierRequest.objects.get(id=request).dossiers.values('barcode')
        registries = Registry.objects.filter(status='creation', dossiers__in=dossiers, type='rc')
    elif registry_type == 'rl':
        registries = Registry.objects.filter(status='creation', type='rl')
    if registries and registries.exists():
        instance = registries.first()
    else:
        instance = Registry.objects.create(**validated_data)
    if dossier not in instance.dossiers.values():
        instance.dossiers.add(dossier)
    task.task_status = 'completed'
    task.save()
    dossier.status = 'Added to registry'
    dossier.save()
    return instance
