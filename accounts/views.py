from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from accounts.serializers.user import AMSUserSerializer, PasswordRecoverySerializer, PasswordConfirmResetSerializer

User = get_user_model()


@extend_schema_view(
    get=extend_schema(summary='Все пользователи', tags=['Users']),
)
class UserListView(generics.ListAPIView):
    queryset = User.objects.exclude(groups__name='Archive clients').exclude(is_active=False).exclude(is_superuser=True)
    permission_classes = [IsAuthenticated]
    serializer_class = AMSUserSerializer


@extend_schema_view(
    post=extend_schema(request=PasswordRecoverySerializer, summary='Восстановление пароля', tags=['Auth']))
class PasswordRecoveryView(APIView):
    serializer_class = PasswordRecoverySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        self.send_recovery_email(user)

        return Response({'message': 'Инструкции по восстановлению пароля отправлены на ваш email.'},
                        status=status.HTTP_200_OK)

    def send_recovery_email(self, user):
        subject = 'Восстановление пароля'
        message = f'Для восстановления пароля перейдите по ссылке: {self.get_recovery_url(user)}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def get_recovery_url(self, user) -> str:
        uidb64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
        token = RefreshToken.for_user(user).access_token
        return f'localhost:5173/reset-password/{uidb64}/{token}/'


@extend_schema_view(
    post=extend_schema(request=PasswordConfirmResetSerializer, summary='Смена пароля', tags=['Auth']))
class PasswordConfirmResetView(APIView):
    serializer_class = PasswordConfirmResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        user_id = force_str(urlsafe_base64_decode(uidb64))

        try:
            token = AccessToken(token)
            token.verify()
        except TokenError:
            return Response({'token': ['Неверный токен для данного пользователя.']},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(summary='Профиль пользователя', tags=['Auth']), )
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = AMSUserSerializer

    def get_object(self):
        return self.request.user
