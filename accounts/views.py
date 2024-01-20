from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from accounts.serializers.user import AMSUserSerializer, ChangePasswordSerializer, RegistrationSerializer

User = get_user_model()


@extend_schema_view(
    get=extend_schema(summary='Все пользователи', tags=['Users']),
)
class UserListView(generics.ListAPIView):
    queryset = User.objects.exclude(groups__name='Archive clients').exclude(is_active=False).exclude(is_superuser=True)
    permission_classes = [IsAuthenticated]
    serializer_class = AMSUserSerializer


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Auth']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


@extend_schema_view(post=extend_schema(request=ChangePasswordSerializer, summary='Смена пароля', tags=['Auth']))
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='Профиль пользователя', tags=['Auth']), )
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = AMSUserSerializer

    def get_object(self):
        return self.request.user
