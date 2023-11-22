from django.urls import path, include
from rest_framework import routers

from logistic.views import ABPlacementView, ABCompletionView

router = routers.SimpleRouter()
router.register(r'placement', ABPlacementView, basename='abplacement')
router.register(r'completion', ABCompletionView, basename='abcompletion')

urlpatterns = [
    path('logistic/', include(router.urls)),
]
