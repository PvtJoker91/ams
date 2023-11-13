from django.urls import path, include
from registration.views import *
from rest_framework import routers



router = routers.SimpleRouter()
router.register(r'ab', ABRegView, basename='abreg')
router.register(r'dossier', DossierRegView, basename='dossierreg')

urlpatterns = [
    path('registration/', include(router.urls)),
    ]