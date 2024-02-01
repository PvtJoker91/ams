from django.utils import timezone

from dossier_requests.models import DossierRequest


def deadline(instance: DossierRequest):
    if not instance:
        return None
    if not instance.time_create:
        return None
    deadline_start = instance.time_create
    workday_start = deadline_start.replace(hour=9, minute=0, second=0)
    workday_end = deadline_start.replace(hour=17, minute=0, second=0)
    if deadline_start.time() < workday_start.time():
        deadline_start = workday_start
    elif deadline_start.time() > workday_end.time():
        deadline_start = workday_start + timezone.timedelta(days=1)
        while deadline_start.weekday() >= 5:
            deadline_start += timezone.timedelta(days=1)
    days_needed = int(instance.urgency) // 8
    remaining_hours = int(instance.urgency) % 8
    deadline = deadline_start + timezone.timedelta(days=days_needed)
    while deadline.weekday() >= 5:
        deadline += timezone.timedelta(days=1)
    if deadline.time() > workday_end.time():
        deadline = deadline.replace(hour=workday_end.hour, minute=workday_end.minute, second=workday_end.second)
    deadline += timezone.timedelta(hours=remaining_hours)
    print(type(deadline))
    return deadline.__format__('%d.%m.%Y %H:%M')