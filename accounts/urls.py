from django.urls import path

from accounts.views import MeView, UserListView, PasswordRecoveryView, PasswordConfirmResetView

urlpatterns = [
    path('users/me/', MeView.as_view(), name='me'),
    path('users/password-recovery/', PasswordRecoveryView.as_view(), name='password-recovery'),
    path('users/password-confirm-reset/', PasswordConfirmResetView.as_view(), name='password-recovery'),
    path('users/list/', UserListView.as_view(), name='user_list'),
]