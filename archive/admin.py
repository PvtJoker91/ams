from django.contrib import admin

from archive.models import Archive, StorageShelf, ArchiveBox, Dossier, Sector, Registry, DossierScan


##############################
# INLINES
##############################
class DossierInline(admin.TabularInline):
    model = Dossier
    fields = ('barcode',)
    readonly_fields = ('barcode',)
    can_delete = False


class ArchiveBoxInline(admin.TabularInline):
    model = ArchiveBox
    fields = ('barcode',)
    readonly_fields = ('barcode',)
    can_delete = False


##############################
# MODELS
##############################


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(StorageShelf)
class StorageShelfAdmin(admin.ModelAdmin):
    list_display = 'shelf_code', 'archive', 'archive_box_number'
    ordering = 'shelf_code',
    inlines = (ArchiveBoxInline,)


@admin.register(ArchiveBox)
class ArchiveBoxAdmin(admin.ModelAdmin):
    list_display = 'barcode', 'current_sector', 'status', 'dossiers_number'
    inlines = (DossierInline,)


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = 'contract', 'barcode', 'current_sector', 'archive_box', 'status',  'storage_address'
    search_fields = 'contract__contract_number',



@admin.register(DossierScan)
class DossierScanAdmin(admin.ModelAdmin):
    list_display = 'dossier', 'file', 'name', 'description'


@admin.register(Registry)
class RegistryAdmin(admin.ModelAdmin):
    list_display = 'type', 'status', 'time_create'
    search_fields = 'dossier__barcode',
    filter_horizontal = 'dossiers', 'checked_dossiers'
