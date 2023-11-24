from django.urls import path, include
from rest_framework import routers

from logistic.views import ABPlacementView, ABCompletionView, DossierCompletionView

router = routers.SimpleRouter()
router.register(r'placement', ABPlacementView, basename='abplacement')
router.register(r'completion', ABCompletionView, basename='abcompletion')
router.register(r'completion/dossier', DossierCompletionView, basename='dossiercompletion')

urlpatterns = [
    path('logistic/', include(router.urls)),
]
