from django.contrib.auth import get_user_model
from rest_framework import serializers

from dossier_requests.models import DossierRequest, DossierTask

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name',
                  'first_name',
                  'email')


class RequestShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = DossierRequest
        fields = (
            'id',
            'status',
            'service',
            'urgency',
            'time_create',
            'description',
        )


class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierTask
        fields = (
            'id',
            'task_status'
        )
