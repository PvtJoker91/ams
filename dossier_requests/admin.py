from django.contrib import admin

from dossier_requests.models import DossierRequest, DossierTask


@admin.register(DossierRequest)
class DossierRequestAdmin(admin.ModelAdmin):
    list_display = (
        'creator', 'client', 'client_department',
        'service', 'urgency', 'time_create',
        'deadline', 'is_expired',
    )
    filter_horizontal = 'dossiers',


@admin.register(DossierTask)
class DossierTaskAdmin(admin.ModelAdmin):
    pass
