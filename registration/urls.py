from django.urls import path, include
from rest_framework import routers

from registration.views import ABRegView, DossierRegView, ContractSearchView

router = routers.SimpleRouter()
router.register(r'ab', ABRegView, basename='abreg')
router.register(r'dossier', DossierRegView, basename='dossierreg')
router.register(r'search', ContractSearchView, basename='contract')

urlpatterns = [
    path('registration/', include(router.urls)),
]
