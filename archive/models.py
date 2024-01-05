from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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

    @property
    def archive_box_number(self):
        return self.archive_box.count()


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
    barcode = models.CharField(max_length=20, verbose_name='Штрих-код АБ')
    current_sector = models.ForeignKey('Sector',
                                       on_delete=models.SET_NULL,
                                       related_name='archive_box',
                                       null=True)
    storage_address = models.ForeignKey('StorageShelf',
                                        verbose_name='Размещение',
                                        on_delete=models.PROTECT,
                                        related_name='archive_box',
                                        blank=True, null=True, default=None)
    status = models.CharField(max_length=30, verbose_name='Статус бокса', blank=True, null=True)

    def __str__(self):
        return f'{self.barcode}'

    class Meta:
        verbose_name = 'Архивный бокс'
        verbose_name_plural = 'Архивные боксы'

    @property
    def dossiers_number(self):
        return self.dossiers.count()


class Dossier(models.Model):
    barcode = models.CharField(primary_key=True,
                               verbose_name='Штрих-код досье',
                               max_length=40,
                               unique=True)
    status = models.CharField(max_length=30, default='На регистрации', verbose_name='Статус досье')
    contract = models.ForeignKey('bank_clients.Contract',
                                 verbose_name='Договор',
                                 on_delete=models.PROTECT,
                                 related_name='dossiers')
    current_sector = models.ForeignKey('Sector',
                                       verbose_name='Расположение',
                                       on_delete=models.SET_NULL,
                                       related_name='dossiers',
                                       null=True, blank=True)
    archive_box = models.ForeignKey('ArchiveBox',
                                    verbose_name='Архивный бокс',
                                    on_delete=models.SET_NULL,
                                    related_name='dossiers',
                                    null=True, blank=True)
    scan_files = models.FileField(upload_to='dossier_scans', blank=True, null=True)

    class Meta:
        verbose_name = 'Досье'
        verbose_name_plural = 'Досье'

    def __str__(self):
        return f'{self.barcode}'

    @property
    def storage_address(self):
        if self.archive_box:
            return self.archive_box.storage_address
        else:
            return None


class Registry(models.Model):
    TYPES = (
        ('lr', 'Logistics to Requests'),
        ('rl', 'Requests to Logistics'),
    )
    STATUSES = (
        ('creation', 'Creation'),
        ('sent', 'Sent'),
        ('on_acceptance', 'On acceptance'),
        ('accepted', 'Accepted'),
    )
    type = models.CharField(choices=TYPES)
    status = models.CharField(choices=STATUSES)
    time_create = models.DateTimeField(auto_now=True)
    dossiers = models.ManyToManyField('Dossier',
                                      verbose_name='Досье',
                                      related_name='registries')
    checked_dossiers = models.ManyToManyField('Dossier',
                                              verbose_name='Сверенные досье',
                                              related_name='registries_checked',
                                              blank=True)
    sender = models.ForeignKey(User,
                               verbose_name='Отправитель',
                               on_delete=models.SET_NULL,
                               related_name='registries',
                               null=True)

    class Meta:
        verbose_name = 'Реестр'
        verbose_name_plural = 'Реестры'

    def __str__(self):
        return f'{self.type}'
