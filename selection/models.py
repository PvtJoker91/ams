from django.contrib.auth import get_user_model
from django.db import models

from archive.models import Dossier

User = get_user_model()


class SelectionOrder(models.Model):
    dossiers = models.ManyToManyField(Dossier, related_name='selecting_order')
    time_create = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='selection_orders', null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_selection_orders', null=True)
