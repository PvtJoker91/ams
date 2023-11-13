from django.db import models


class Client(models.Model):
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    name = models.CharField(max_length=30, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    passport = models.CharField(max_length=30, verbose_name='Номер паспорта')
    birthday = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.last_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Contract(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Договор')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='contracts', verbose_name='Клиент')
    contract_number = models.CharField(max_length=10, verbose_name='Номер договора')
    time_create = models.DateField(verbose_name='Дата заключения')
    barcode = models.CharField(max_length=40, verbose_name='Штрих-код договора', null=True, blank=True, unique=True)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return self.product.name
