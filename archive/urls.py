from django.urls import path, include
from rest_framework import routers

from archive.views.dossiers import DossierView, DossiersListUpdateView

router = routers.SimpleRouter()
router.register(r'dossier', DossierView, basename='dossier')

urlpatterns = [
    path('units/', include(router.urls)),
    path('units/dossiers_to_update', DossiersListUpdateView.as_view(), name='update_dossier_list'),
]
