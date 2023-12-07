from django.urls import path, include
from rest_framework import routers

from logistics.views.archive_box import ABPlacementView, ABCompletionView, ABCheckView
from logistics.views.dossier import DossierCheckView, DossierCompletionView

router = routers.SimpleRouter()
router.register(r'placement', ABPlacementView, basename='abplacement')
router.register(r'checking', ABCheckView, basename='abcheck')
router.register(r'completion', ABCompletionView, basename='abcompletion')
router.register(r'checking/dossier', DossierCheckView, basename='dossiercompletion')
router.register(r'completion/dossier', DossierCompletionView, basename='dossiercompletion')

urlpatterns = [
    path('logistics/', include(router.urls)),
]
