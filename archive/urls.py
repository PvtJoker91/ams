from django.urls import path, include
from rest_framework import routers

from archive.views.units import DossierSearchView

router = routers.SimpleRouter()
router.register(r'dossier', DossierSearchView, basename='dossier')

urlpatterns = [
    path('units/', include(router.urls)),
]
