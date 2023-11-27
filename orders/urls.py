from django.urls import path, include
from rest_framework import routers
from orders.views import DossierSearchView, OrderView

router = routers.SimpleRouter()
router.register(r'search', DossierSearchView, basename='orders_dossier_search')
router.register(r'', OrderView, basename='orders_create')


urlpatterns = [
    path('orders/', include(router.urls)),
    ]