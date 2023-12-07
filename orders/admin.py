from django.contrib import admin

from orders.models import DossierOrder


@admin.register(DossierOrder)
class DossierOrderAdmin(admin.ModelAdmin):
    list_display = (
        'creator', 'client', 'client_department',
        'service', 'urgency', 'time_create',
        'deadline', 'is_expired',
    )
    filter_horizontal = 'dossiers',

