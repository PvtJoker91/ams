from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserOrderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name',
                  'first_name',
                  'email')
