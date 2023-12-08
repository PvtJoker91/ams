from django.urls import path

from accounts.views import me

urlpatterns = [
    path('me/', me, name='me'),
]