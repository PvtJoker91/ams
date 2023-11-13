from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from registration.urls import urlpatterns as registration_urls
from bank_clients.urls import urlpatterns as bank_clients_urls


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += registration_urls
urlpatterns += bank_clients_urls
