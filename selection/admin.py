from django.contrib import admin

from selection.models import SelectionOrder


@admin.register(SelectionOrder)
class SelectionOrderAdmin(admin.ModelAdmin):
    list_display = ('time_create',)
    # filter_horizontal = 'tasks',