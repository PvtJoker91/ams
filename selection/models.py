from django.contrib.auth import get_user_model
from django.db import models


from dossier_requests.models import DossierTask

User = get_user_model()


class SelectionOrder(models.Model):
    tasks = models.ManyToManyField(DossierTask, related_name='selection_orders')
    time_create = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='selection_orders', null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_selection_orders', null=True)
    selected = models.SmallIntegerField(default=0)
