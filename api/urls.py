from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from registration.urls import urlpatterns as registration_urls
from logistics.urls import urlpatterns as logistic_urls
from orders.urls import urlpatterns as orders_urls
from archive.urls import urlpatterns as units_urls
from accounts.urls import urlpatterns as accounts_urls
from bank_clients.urls import urlpatterns as bank_clients_urls
from selection.urls import urlpatterns as selection_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += registration_urls
urlpatterns += logistic_urls
urlpatterns += orders_urls
urlpatterns += selection_urls
urlpatterns += units_urls
urlpatterns += accounts_urls
urlpatterns += bank_clients_urls
