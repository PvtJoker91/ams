import datetime

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


    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'{self.product.name} | {self.client.last_name} {self.client.name}'


# Заполнение банковской базы

# def fill_clients(quantity):
#     import random
#     import datetime
#
#     names = 'Александр,Дмитрий,Максим,Сергей,Андрей,Алексей,Артём,Илья,Кирилл,Михаил,Никита,Матвей,Роман,Егор,Арсений,Иван,' \
#             'Денис,Евгений,Даниил,Тимофей,Владислав,Игорь,Владимир,Павел,Руслан,Марк,Константин,Тимур,Олег,Ярослав,Антон,Николай,' \
#             'Глеб,Данил,Савелий,Вадим,Степан,Юрий,Богдан,Артур,Семен,Макар,Лев,Виктор,Елисей,Виталий,Вячеслав,Захар,Мирон,Дамир,Георгий,' \
#             'Давид,Платон,Анатолий,Григорий,Демид,Данила,Станислав,Василий,Федор,Родион,Леонид,Одиссей,Валерий,Святослав,Борис,Эдуард,Марат'.split(',')
#
#     second_names = 'Иванов,Смирнов,Кузнецов,Попов,Васильев,Петров,Соколов,Михайлов,Новиков,Федоров,' \
#                    'Морозов,Волков,Алексеев,Лебедев,Семенов,Егоров,Павлов,Козлов,Степанов,Николаев,Орлов,Андреев,' \
#                    'Макаров,Никитин,Захаров,Зайцев,Соловьев,Борисов,Яковлев,Григорьев,Романов,Воробьев,Сергеев,Кузьмин,' \
#                    'Фролов,Александров,Дмитриев,Королев,Гусев,Киселев,Ильин,Максимов,Поляков,Сорокин,Виноградов,Ковалев,Белов,Медведев,Антонов,Тарасов'.split(',')
#
#     third_names = 'Александрович,Дмитриевич,Максимович,Сергеевич,Андреевич,Алексеевич,Артёмович,Ильич,Кириллович,Михаилович,Никитович,Матвеевич,Романович,Егорович,Арсениевич,Иванович,' \
#             'Денисович,Евгениевич,Даниилович,Тимофеевич,Владиславович,Игоревич,Владимирович,Павлович,Русланович,Маркович,Константинович,Тимурович,Олегович,Ярославович,Антонович,Николаевич,' \
#             'Глебович,Данилович,Савелиевич,Вадимович,Степанович,Юрьевич,Богданович,Артурович,Семенович,Макарович,Викторович,Виталий,Вячеславович,Захарович,Миронович,Дамирович,' \
#             'Давидович,Платонович,Анатолиевич,Григориевич,Демидович,Данилович,Станиславович,Василиевич,Федорович,Родионович,Леонидович,Одиссеевич,Валериевич,Святославович,Борисович,Эдуардович,Маратович'.split(',')
#
#     for client in range(quantity):
#         Client.objects.create(name=random.choice(names),
#                               last_name=random.choice(second_names),
#                               middle_name=random.choice(third_names),
#                               passport=random.randint(1000000, 9999999),
#                               birthday=f'{random.randint(1930,2005)}-0{random.randint(1,9)}-{random.randint(10,28)}'
#                               )
#
#
# def fill_contracts(quantity):
#     import random
#
#     for contract in range(quantity):
#         Contract.objects.create(product_id=Product.objects.all()[random.randint(0, 4)].id,
#                               client_id=Client.objects.all()[random.randint(0, 49)].id,
#                               contract_number=str(random.randint(1000000, 9999999)),
#                               time_create=datetime.date.today()
#                               )