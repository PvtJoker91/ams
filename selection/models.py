from django.contrib.auth import get_user_model
from django.db import models

from archive.models import Dossier
from dossier_requests.models import DossierTask

User = get_user_model()


class SelectionOrder(models.Model):
    tasks = models.ManyToManyField(DossierTask, related_name='selection_orders')
    selected = models.ManyToManyField(Dossier, related_name='selection_orders')
    time_create = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='selection_orders', null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_selection_orders', null=True)


    class Meta:
        verbose_name = 'Наряд на подбор'
        verbose_name_plural = 'Наряды на подбор'