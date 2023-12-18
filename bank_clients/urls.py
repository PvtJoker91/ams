from django.urls import path, include
from rest_framework import routers

from bank_clients.views import ContractView

router = routers.SimpleRouter()
router.register(r'', ContractView, basename='contracts_search')


urlpatterns = [
    path('contracts/', include(router.urls)),
    ]