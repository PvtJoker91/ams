from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from accounts.models.users import AMSGroup

User = get_user_model()


class AMSGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AMSGroup
        fields = 'name',


class AMSUserSerializer(serializers.ModelSerializer):
    groups = AMSGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'is_superuser'


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordConfirmResetSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        validate_password(new_password)
        return super().validate(attrs)

