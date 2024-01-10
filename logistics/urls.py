from django.urls import path, include
from rest_framework import routers

from logistics.views.placement import ABPlacementView
from logistics.views.completion import DossierCompletionView, ABCompletionView
from logistics.views.checking import DossierCheckView, ABCheckView


router = routers.SimpleRouter()
router.register(r'checking', ABCheckView, basename='abcheck')
router.register(r'completion', ABCompletionView, basename='abcompletion')
router.register(r'checking/dossier', DossierCheckView, basename='dossierchecking')
router.register(r'completion/dossier', DossierCompletionView, basename='dossiercompletion')

urlpatterns = [
    path('logistics/', include(router.urls)),
    path('logistics/placement', ABPlacementView.as_view(), name='abplacement'),
]
