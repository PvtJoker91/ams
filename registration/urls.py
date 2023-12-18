from django.urls import path, include
from rest_framework import routers

from registration.views import ABRegView, DossierRegView

router = routers.SimpleRouter()
router.register(r'ab', ABRegView, basename='abreg')
router.register(r'dossier', DossierRegView, basename='dossierreg')

urlpatterns = [
    path('registration/', include(router.urls)),
]
