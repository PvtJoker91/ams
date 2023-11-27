from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from common_archive.models import Dossier

SERVICE_TYPES = (
    ('1', 'Full scanning'),
    ('2', 'Scanning by documents'),
    ('3', 'Temporary issuance'),
    ('4', 'Unrecoverable issuance')
)

URGENCY_TYPES = (
    ('40', 'Standard - 40 w.h.'),
    ('16', 'Increased - 16 w.h.'),
    ('8', 'High - 8 w.h.'),
)

ORDER_STATUSES = (
    ('1', 'Creation'),
    ('2', 'Sent for processing'),
    ('3', 'Accepted'),
    ('4', 'Rejected'),
    ('5', 'Sent for selection'),
    ('6', 'On selection'),
    ('7', 'Sent for scanning'),
    ('8', 'On scanning'),
    ('9', 'Complete'),
)


class DossierOrder(models.Model):
    status = models.CharField(choices=ORDER_STATUSES)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
    client = models.CharField(max_length=50)
    client_department = models.CharField(max_length=100)
    service = models.CharField(choices=SERVICE_TYPES)
    urgency = models.CharField(choices=URGENCY_TYPES)
    description = models.TextField()
    time_create = models.DateTimeField(auto_now=True)
    dossiers = models.ManyToManyField(Dossier, related_name='orders')

    def __str__(self):
        return f'{self.service} {self.client_department}'

    @property
    def deadline(self):
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
        return self.deadline < timezone.now()

