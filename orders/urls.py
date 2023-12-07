from django.urls import path, include
from rest_framework import routers
from orders.views import OrderView

router = routers.SimpleRouter()
router.register(r'', OrderView, basename='orders_create')


urlpatterns = [
    path('orders/', include(router.urls)),
    ]