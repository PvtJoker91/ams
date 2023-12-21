from django.contrib import admin

from orders.models import DossiersOrder, DossierTask


@admin.register(DossiersOrder)
class DossierOrderAdmin(admin.ModelAdmin):
    list_display = (
        'creator', 'client', 'client_department',
        'service', 'urgency', 'time_create',
        'deadline', 'is_expired',
    )
    filter_horizontal = 'dossiers',


@admin.register(DossierTask)
class DossierTaskAdmin(admin.ModelAdmin):
    pass
