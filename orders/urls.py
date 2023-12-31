from django.urls import path, include
from rest_framework import routers
from orders.views.orders import OrderView, MyOrdersView
from orders.views.tasks import TaskView, TaskListUpdateView

router = routers.SimpleRouter()
router.register(r'orders', OrderView, basename='orders')
router.register(r'myorders', MyOrdersView, basename='my_orders')
router.register(r'tasks', TaskView, basename='tasks')


urlpatterns = [
    path('orders/', include(router.urls)),
    path('orders/tasks/list_update', TaskListUpdateView.as_view(), name='task_list_update'),
]