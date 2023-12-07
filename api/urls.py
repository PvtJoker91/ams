from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from registration.urls import urlpatterns as registration_urls
from logistic.urls import urlpatterns as logistic_urls
from orders.urls import urlpatterns as orders_urls
from archive.urls import urlpatterns as units_urls


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += registration_urls
urlpatterns += logistic_urls
urlpatterns += orders_urls
urlpatterns += units_urls
