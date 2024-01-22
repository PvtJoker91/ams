from django.urls import path, include
from rest_framework import routers

from archive.views.dossiers import DossierView, DossierScanView
from archive.views.registries import RegistryView

router = routers.SimpleRouter()
router.register(r'dossier', DossierView, basename='dossier')
router.register(r'scans', DossierScanView, basename='dossier-scan')
router.register(r'registry', RegistryView, basename='registry')

urlpatterns = [
    path('units/', include(router.urls)),
]
