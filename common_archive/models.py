from django.db import models


class Archive(models.Model):
    code = models.PositiveSmallIntegerField(verbose_name='Код')
    name = models.CharField(max_length=50, verbose_name='Название архива')
    address = models.CharField(max_length=255, verbose_name='Адрес архива')

    class Meta:
        verbose_name = 'Архив'
        verbose_name_plural = 'Архивы'

    def __str__(self):
        return self.name


class StorageShelf(models.Model):
    archive = models.ForeignKey('Archive', models.CASCADE, related_name='storage', verbose_name='Архив')
    shelf_code = models.CharField(max_length=20, verbose_name='Код полки')

    class Meta:
        verbose_name = 'Полка хранилища'
        verbose_name_plural = 'Полки хранилища'

    def __str__(self):
        return self.shelf_code


def fill_storage():
    archive_code = '10'
    levels = ['01', '02']
    rooms = ['01', '02']
    rows = ['A', 'B', 'C', 'D']
    racks = ['01', '02', '03']
    shelfs = ['01', '02', '03']

    for level in levels:
        for room in rooms:
            for row in rows:
                for rack in racks:
                    for shelf in shelfs:
                        StorageShelf.objects.create(archive_id=Archive.objects.all()[0].id,
                                                    shelf_code=f'{archive_code}.{level}.{room}.-{row}.{rack}.{shelf}')
    return


class Sector(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Сектор'
        verbose_name_plural = 'Секторы'

    def __str__(self):
        return self.name


class ArchiveBox(models.Model):
    barcode = models.CharField(max_length=20, verbose_name='Штрих-код АБ', unique=True)
    current_sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, related_name='archive_box', null=True)
    storage_address = models.ForeignKey('StorageShelf', on_delete=models.PROTECT, related_name='archive_box',
                                        verbose_name='Размещение', null=True, default=None)

    def __str__(self):
        return f'{self.barcode}'

    class Meta:
        verbose_name = 'Архивный бокс'
        verbose_name_plural = 'Архивные боксы'


class FileBox(models.Model):
    barcode = models.CharField(max_length=20, verbose_name='Штрих-код ФБ', unique=True)
    archive_box = models.ForeignKey('ArchiveBox', on_delete=models.PROTECT, default=None, related_name='file_box')
    current_sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, related_name='file_box', null=True)

    def __str__(self):
        return f'{self.barcode}'

    class Meta:
        verbose_name = 'Файловый бокс'
        verbose_name_plural = 'Файловые боксы'


class Dossier(models.Model):
    contract = models.ForeignKey('bank_clients.Contract', on_delete=models.PROTECT, related_name='dossiers',
                                 verbose_name='Досье', null=True, blank=True)
    barcode = models.CharField(max_length=40, verbose_name='Штрих-код досье', unique=True)
    current_sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, related_name='dossiers',
                                       verbose_name='Расположение', null=True)
    status = models.CharField(max_length=30, default='На регистрации', verbose_name='Статус досье')
    archive_box = models.ForeignKey(
        'ArchiveBox', on_delete=models.PROTECT,
        verbose_name='Архивный бокс', related_name='dossiers',
        null=True, blank=True
    )
    file_box = models.ForeignKey(
        'FileBox', on_delete=models.PROTECT,
        verbose_name='Файловый бокс', related_name='dossiers',
        null=True, blank=True,

    )

    class Meta:
        verbose_name = 'Досье'
        verbose_name_plural = 'Досье'

    def __str__(self):
        return f'{self.contract.product.name} {self.barcode}'