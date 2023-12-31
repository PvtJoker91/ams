from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from archive.models import Dossier

User = get_user_model()


class DossiersOrder(models.Model):
    SERVICE_TYPES = (
        ('full_scanning', 'Full scanning'),
        ('scanning_by_documents', 'Scanning by documents'),
        ('temporary_issuance', 'Temporary issuance'),
        ('unrecoverable_issuance', 'Unrecoverable issuance')
    )

    URGENCY_HOURS = (
        ('40', 'Standard - 40 w.h.'),
        ('16', 'Increased - 16 w.h.'),
        ('8', 'High - 8 w.h.'),
    )

    ORDER_STATUSES = (
        ('creation', 'Creation'),
        ('sent_for_processing', 'Sent for processing'),
        ('cancelled', 'Cancelled'),
        ('accepted', 'Accepted'),
        ('sent_for_selection', 'Sent for selection'),
        ('on_selection', 'On selection'),
        ('sent_for_scanning', 'Sent for scanning'),
        ('on_scanning', 'On scanning'),
        ('complete', 'Complete'),
    )

    status = models.CharField(choices=ORDER_STATUSES)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
    closer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='closed_orders', blank=True, null=True)
    client = models.CharField(max_length=50)
    client_department = models.CharField(max_length=100)
    service = models.CharField(choices=SERVICE_TYPES)
    urgency = models.CharField(choices=URGENCY_HOURS)
    description = models.TextField()
    close_reason = models.TextField(null=True, blank=True)
    time_create = models.DateTimeField(null=True, blank=True)
    time_close = models.DateTimeField(null=True, blank=True)
    dossiers = models.ManyToManyField(Dossier, related_name='orders', blank=True)

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
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('on_selection', 'On selection'),
        ('on_scanning', 'On scanning'),
        ('completed', 'Completed'),
    )
    dossier = models.ForeignKey(Dossier, on_delete=models.PROTECT, related_name='tasks')
    order = models.ForeignKey(DossiersOrder, on_delete=models.CASCADE, related_name='tasks')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True)
    task_status = models.CharField(choices=TASK_STATUSES)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.task_status
