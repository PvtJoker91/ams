from django.urls import path, include
from rest_framework import routers
from selection.views import DossierSelectingView, SelectionOrderView, TaskSelectingView, RegistrySelectionView

router = routers.SimpleRouter()
router.register(r'dossier', DossierSelectingView, basename='dossier_selecting')
router.register(r'orders', SelectionOrderView, basename='selection_orders')
router.register(r'tasks', TaskSelectingView, basename='tasks_selecting')
router.register(r'registry', RegistrySelectionView, basename='lr_registry')



urlpatterns = [
    path('selection/', include(router.urls)),
]