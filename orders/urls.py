from django.urls import path, include
from rest_framework import routers
from orders.views.orders import OrderView


router = routers.SimpleRouter()
router.register(r'', OrderView, basename='orders')


urlpatterns = [
    path('orders/', include(router.urls)),
    ]