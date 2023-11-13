from django.urls import path, include
from rest_framework import routers

from bank_clients.views import ContractSearchView

router = routers.SimpleRouter()
router.register(r'', ContractSearchView, basename='contract')


urlpatterns = [
    path('search/', include(router.urls)),
    ]