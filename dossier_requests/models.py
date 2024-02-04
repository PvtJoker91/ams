from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from archive.models import Dossier

User = get_user_model()


class DossierRequest(models.Model):
    SERVICE_TYPES = (
        ('full_scanning', 'Сканирование в один файл'),
        ('scanning_by_documents', 'Сканирование по документам'),
        ('temporary_issuance', 'Выдача во временное пользование'),
        ('unrecoverable_issuance', 'Безвозвратная выдача')
    )

    URGENCY_HOURS = (
        ('40', 'Стандартная - 40 р.ч.'),
        ('16', 'Повышенная - 16 р.ч.'),
        ('8', 'Срочная - 8 р.ч.'),
    )

    REQUEST_STATUSES = (
        ('creation', 'Создание'),
        ('sent_for_processing', 'Отправлена в архив'),
        ('cancelled', 'Отменена'),
        ('accepted', 'Принята к исполнению'),
        ('in_progress', 'В работе'),
        ('complete', 'Завершена'),
    )

    status = models.CharField(choices=REQUEST_STATUSES)
    service = models.CharField(choices=SERVICE_TYPES)
    urgency = models.CharField(choices=URGENCY_HOURS)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='requests', null=True)
    closer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='closed_requests', blank=True, null=True)
    client = models.CharField(max_length=50)
    client_department = models.CharField(max_length=100)
    description = models.TextField()
    close_reason = models.TextField(null=True, blank=True)
    time_create = models.DateTimeField(null=True, blank=True)
    time_close = models.DateTimeField(null=True, blank=True)
    dossiers = models.ManyToManyField(Dossier, related_name='requests', blank=True)

    class Meta:
        verbose_name = 'Заявка на досье'
        verbose_name_plural = 'Заявки на досье'

    def __str__(self):
        return f'{self.service} {self.client_department}'

    @property
    def deadline(self):
        if not self.time_create:
            return None
        deadline_start = self.time_create
        workday_start = deadline_start.replace(hour=9, minute=0, second=0)
        workday_end = deadline_start.replace(hour=17, minute=0, second=0)
        if deadline_start.time() < workday_start.time():
            deadline_start = workday_start
        elif deadline_start.time() > workday_end.time():
            deadline_start = workday_start + timezone.timedelta(days=1)
            while deadline_start.weekday() >= 5:
                deadline_start += timezone.timedelta(days=1)
        days_needed = int(self.urgency) // 8
        remaining_hours = int(self.urgency) % 8
        deadline = deadline_start + timezone.timedelta(days=days_needed)
        while deadline.weekday() >= 5:
            deadline += timezone.timedelta(days=1)
        if deadline.time() > workday_end.time():
            deadline = deadline.replace(hour=workday_end.hour, minute=workday_end.minute, second=workday_end.second)
        deadline += timezone.timedelta(hours=remaining_hours)
        return deadline

    @property
    def is_expired(self):
        return self.deadline < timezone.now() if self.deadline else None


class DossierTask(models.Model):
    TASK_STATUSES = (
        ('accepted', 'Принято в работу'),
        ('cancelled', 'Отменено'),
        ('on_selection', 'На подборе'),
        ('selected', 'Подобрано'),
        ('rejected', 'Отклонено'),
        ('completed', 'Исполнено'),
    )
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='tasks')
    request = models.ForeignKey(DossierRequest, on_delete=models.CASCADE, related_name='tasks')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True)
    task_status = models.CharField(choices=TASK_STATUSES)
    commentary = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Задание по заявке'
        verbose_name_plural = 'Задания по заявкам'

    def __str__(self):
        return self.task_status


