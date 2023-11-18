from django.contrib import admin

from bank_clients.models import Client, Contract, Product


##############################
# INLINES
##############################
class ContractInline(admin.TabularInline):
    model = Contract
    fields = ('product', 'contract_number', 'time_create',)
    readonly_fields = ('product', 'contract_number', 'time_create',)
    can_delete = False




##############################
# MODELS
##############################
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('product', 'client', 'contract_number', 'time_create',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'name', 'middle_name', 'passport', 'birthday')
    inlines = (ContractInline,)


admin.site.register(Product)


