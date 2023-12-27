from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from orders.models import DossiersOrder, DossierTask

User = get_user_model()


class UserShortSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name',
                  'first_name',
                  'email')


class OrderShortSerializer(ModelSerializer):
    class Meta:
        model = DossiersOrder
        fields = (
            'id',
            'status',
            'service',
            'urgency',
            'time_create',
        )


class TaskShortSerializer(ModelSerializer):
    class Meta:
        model = DossierTask
        fields = (
            'id',
            'task_status'
        )
