from django.contrib import admin

from common_archive.models import Archive, StorageShelf, ArchiveBox, FileBox, Dossier, Sector


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(StorageShelf)
class StorageShelfAdmin(admin.ModelAdmin):
    list_display = 'shelf_code', 'archive'
    ordering = 'shelf_code',


@admin.register(ArchiveBox)
class ArchiveBoxAdmin(admin.ModelAdmin):
    list_display = 'barcode', 'current_sector'

@admin.register(FileBox)
class FileBoxAdmin(admin.ModelAdmin):
    list_display = 'barcode', 'archive_box', 'current_sector'

@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = 'contract', 'barcode', 'current_sector', 'status', 'archive_box', 'file_box'

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = 'name',

