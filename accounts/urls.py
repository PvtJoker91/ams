from django.urls import path

from accounts.views import MeView, RegistrationView, ChangePasswordView

urlpatterns = [
    path('users/me/', MeView.as_view(), name='me'),
    path('users/reg/', RegistrationView.as_view(), name='reg'),
    path('users/change-passwd/', ChangePasswordView.as_view(), name='change_passwd'),
]