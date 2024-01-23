from django.urls import path, include
from rest_framework import routers

from archive.views.archive_box import ABDetailView
from archive.views.dossiers import DossierView, DossierScanView
from archive.views.registries import RegistryView

router = routers.SimpleRouter()
router.register(r'dossier', DossierView, basename='dossier')
router.register(r'scans', DossierScanView, basename='dossier-scan')
router.register(r'registry', RegistryView, basename='registry')
router.register(r'archive-box', ABDetailView, basename='ab-detail')

urlpatterns = [
    path('units/', include(router.urls)),
]
