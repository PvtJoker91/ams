from django.urls import path, include
from rest_framework import routers

from registration.views import ABRegView, DossierRegView

router = routers.SimpleRouter()
router.register(r'ab', ABRegView, basename='ab-reg')
router.register(r'dossier', DossierRegView, basename='dossier-reg')

urlpatterns = [
    path('registration/', include(router.urls)),
]
