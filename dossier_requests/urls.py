from django.urls import path, include
from rest_framework import routers

from dossier_requests.views.requests import MyRequestsView, RequestView
from dossier_requests.views.tasks import TaskView, TaskExecuteView

router = routers.SimpleRouter()
router.register(r'requests', RequestView, basename='requests')
router.register(r'my-requests', MyRequestsView, basename='my_requests')
router.register(r'tasks', TaskView, basename='tasks')
router.register(r'execute-tasks', TaskExecuteView, basename='tasks_to_execute')

urlpatterns = [
    path('requests/', include(router.urls)),
]
