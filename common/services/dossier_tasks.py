from rest_framework.exceptions import ParseError

from archive.models import Dossier
from dossier_requests.models import DossierTask
from selection.models import SelectionOrder


def change_tasks_status_while_dossier_selecting(instance: Dossier) -> None:
    """ Получаем таски по досье. Меняем статус тасков и добавляем досье в "selected" у наряда. """

    tasks = DossierTask.objects.filter(dossier=instance, task_status='on_selection')
    if not tasks.exists():
        raise ParseError(f'Dossier is not in any task')
    for task in tasks:
        orders = SelectionOrder.objects.filter(tasks=task)
        for order in orders:
            order.selected.add(task.dossier)
        task.task_status = 'selected'
        task.save()


def change_tasks_status_while_order_creation(tasks: list) -> None:
    task_ids = [task.id for task in tasks]
    task_instances = DossierTask.objects.filter(id__in=task_ids)
    task_instances.update(task_status='on_selection')
