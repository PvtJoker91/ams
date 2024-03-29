from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    permission_classes = [AllowAny]
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # token['first_name'] = user.first_name
        # token['last_name'] = user.last_name
        # token['email'] = user.email



        return token