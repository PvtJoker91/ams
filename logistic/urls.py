from django.urls import path, include
from rest_framework import routers

from logistic.views import *

router = routers.SimpleRouter()
router.register(r'ab', ABPlacementView, basename='abplacement')

urlpatterns = [
    path('logistic/', include(router.urls)),
]
