from django.urls import path, include
from rest_framework import routers

from dossier_requests.views.registries import RegistryRequestsView
from dossier_requests.views.requests import MyRequestsView, RequestView
from dossier_requests.views.tasks import TaskListUpdateView, TaskView, TaskExecuteView

router = routers.SimpleRouter()
router.register(r'requests', RequestView, basename='requests')
router.register(r'my-requests', MyRequestsView, basename='my_requests')
router.register(r'tasks', TaskView, basename='tasks')
router.register(r'execute-tasks', TaskExecuteView, basename='tasks_to_execute')
router.register(r'registry', RegistryRequestsView, basename='registry_requests')


urlpatterns = [
    path('requests/', include(router.urls)),
    path('requests/tasks/list_update', TaskListUpdateView.as_view(), name='task_list_update'),
]