from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from api.test_views import  test_reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('test2/', test_reg),
]
