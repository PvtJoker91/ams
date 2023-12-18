from django.urls import path, include
from rest_framework import routers

from archive.views import DossierView

router = routers.SimpleRouter()
router.register(r'dossier', DossierView, basename='dossier')

urlpatterns = [
    path('units/', include(router.urls)),
]
