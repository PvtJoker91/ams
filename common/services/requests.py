from dossier_requests.models import DossierTask


def change_request_status(instance: DossierTask) -> None:
    """ Получаем запрос по таску. Меняем статус запроса. """
    request = instance.request
    uncomplete_tasks = request.tasks.filter(task_status__in=('accepted', 'on_selection', 'selected'))
    if not uncomplete_tasks.exists():
        request.status = 'complete'
        request.save()
    else:
        if request.status != 'in_progress':
            request.status = 'in_progress'
            request.save()
