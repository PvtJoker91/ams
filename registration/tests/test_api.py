import json

from django.contrib.auth import get_user_model

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.users import AMSGroup
from archive.models import ArchiveBox, Dossier, Sector
from bank_clients.models import Client, Product, Contract

User = get_user_model()


class RegistrationTestCase(APITestCase):
    """Тестирование CRUD"""

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.group = AMSGroup.objects.create(name='Registration')
        self.user.groups.add(self.group)
        self.bank_client = Client.objects.create(last_name='Ivanov',
                                                 first_name='Ivan',
                                                 middle_name='Ivanovich',
                                                 passport='222222',
                                                 birthday='2000-01-01')
        self.product = Product.objects.create(name='Credit')
        self.contract = Contract.objects.create(product=self.product,
                                                client=self.bank_client,
                                                contract_number='10000001',
                                                time_create=timezone.now())
        self.sector = Sector.objects.create(name='Registration')
        self.archive_box1 = ArchiveBox.objects.create(barcode='AB-00-000001',
                                                      current_sector=self.sector,
                                                      status='На регистрации')
        self.archive_box2 = ArchiveBox.objects.create(barcode='AB-00-000002',
                                                      current_sector=self.sector,
                                                      status='На регистрации')
        self.archive_box3 = ArchiveBox.objects.create(barcode='AB-00-000003',
                                                      current_sector=self.sector,
                                                      status='На регистрации')

        self.dossier1 = Dossier.objects.create(barcode='D00-00-00000001',
                                               status='На регистрации',
                                               current_sector=self.sector,
                                               contract=self.contract,
                                               archive_box=self.archive_box1,
                                               registerer=self.user)


    def test_box_create(self):
        self.assertEqual(3, ArchiveBox.objects.all().count())
        url = '/api/registration/ab/'
        data = {
            'barcode': 'AB-11-000004',
            'current_sector': 1,
            'status': 'On registration',
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, ArchiveBox.objects.all().count())


    def test_dossier_create(self):
        self.assertEqual(1, Dossier.objects.all().count())
        url = '/api/registration/dossier/'
        data = {
            'barcode': 'D11-00-00000001',
            'status': 'On registration',
            'contract': self.contract.id,
            'current_sector': self.sector.id,
            'archive_box': self.archive_box1.id,
            'registerer': self.user.id
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Dossier.objects.all().count())
        self.assertEqual(self.archive_box1, Dossier.objects.last().archive_box)
        self.assertEqual(self.contract, Dossier.objects.last().contract)
        self.assertEqual(self.sector, Dossier.objects.last().current_sector)
        self.assertEqual(self.user, Dossier.objects.last().registerer)

#     def test_update(self):
#         url = reverse('book-detail', args=(self.book_1.id,))
#         data = {'name': self.book_1.name,
#                 'price': '1500',
#                 'author': self.book_1.author.id,
#                 'category': self.book_1.category.id
#                 }
#         json_data = json.dumps(data)
#         self.client.force_login(self.user)
#         response = self.client.put(url, data=json_data,
#                                    content_type='application/json')
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.book_1.refresh_from_db()
#         self.assertEqual(1500, self.book_1.price)
#
#     def test_get(self):
#         url = reverse('book-list')
#         response = self.client.get(url)
#         books = Book.objects.annotate(
#             likes=Count('userbookrelation', filter=Q(userbookrelation__like=True)),
#             rating=Avg('userbookrelation__rate'),
#             price_discount=F('price') * (1 - F('discount'))).order_by('id')
#         serializer_data = BookSerializer(books, many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)
#         self.assertEqual(serializer_data[0]['rating'], '5.00')
#         self.assertEqual(serializer_data[0]['likes'], 1)
#
#     def test_filter(self):
#         url = reverse('book-list')
#         response = self.client.get(url, data={'price': 50})
#         books = Book.objects.filter(id__in=[self.book_1.id, self.book_2.id]).annotate(
#             likes=Count('userbookrelation', filter=Q(userbookrelation__like=True)),
#             rating=Avg('userbookrelation__rate'),
#             price_discount=F('price') * (1 - F('discount'))).order_by('id')
#         serializer_data = BookSerializer(books, many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)
#
#     def test_search(self):
#         url = reverse('book-list')
#         response = self.client.get(url, data={'search': 'Author1'})
#         books = Book.objects.filter(id__in=[self.book_1.id, self.book_2.id]).annotate(
#             likes=Count('userbookrelation', filter=Q(userbookrelation__like=True)),
#             rating=Avg('userbookrelation__rate'),
#             price_discount=F('price') * (1 - F('discount'))).order_by('id')
#         serializer_data = BookSerializer(books, many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)
#
#     def test_delete(self):
#         self.assertEqual(3, Book.objects.all().count())
#         url = reverse('book-detail', args=(self.book_1.id,))
#         self.client.force_login(self.user)
#         response = self.client.delete(url)
#         self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
#         self.assertEqual(2, Book.objects.all().count())
#
#     def test_update_not_owner(self):
#         self.user2 = User.objects.create(username='test_username2')
#         url = reverse('book-detail', args=(self.book_1.id,))
#         data = {'name': self.book_1.name,
#                 'price': '1500',
#                 'author': self.book_1.author.id,
#                 'category': self.book_1.category.id
#                 }
#         json_data = json.dumps(data)
#         self.client.force_login(self.user2)
#         response = self.client.put(url, data=json_data,
#                                    content_type='application/json')
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
#         self.book_1.refresh_from_db()
#         self.assertEqual(50, self.book_1.price)
#
#     def test_update_not_owner_but_staff(self):
#         self.user2 = User.objects.create(username='test_username2',
#                                          is_staff=True)
#         url = reverse('book-detail', args=(self.book_1.id,))
#         data = {'name': self.book_1.name,
#                 'price': '1500',
#                 'author': self.book_1.author.id,
#                 'category': self.book_1.category.id
#                 }
#         json_data = json.dumps(data)
#         self.client.force_login(self.user2)
#         response = self.client.put(url, data=json_data,
#                                    content_type='application/json')
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.book_1.refresh_from_db()
#         self.assertEqual(1500, self.book_1.price)
#
#
# class BooksRelationTestCase(APITestCase):
#     '''Тестирование функционала "Like", "Закладки", "Рейтинг"'''
#
#     def setUp(self):
#         self.user = User.objects.create(username='test_username')
#         self.user2 = User.objects.create(username='test_username2')
#         self.book = Book.objects.create(name='TestBook', price=25)
#
#     def test_like(self):
#         url = reverse('userbookrelation-detail', args=(self.book.id,))
#         self.client.force_login(self.user)
#         data = {
#             'like': True,
#             'in_bookmarks': True
#         }
#         json_data = json.dumps(data)
#         response = self.client.patch(url, data=json_data,
#                                      content_type='application/json')
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         relation = UserBookRelation.objects.get(user=self.user, book=self.book)
#         self.assertTrue(relation.like)
#         self.assertTrue(relation.in_bookmarks)
#
#     def test_rate(self):
#         url = reverse('userbookrelation-detail', args=(self.book.id,))
#         self.client.force_login(self.user)
#         data = {
#             'rate': 4
#         }
#         json_data = json.dumps(data)
#         response = self.client.patch(url, data=json_data,
#                                      content_type='application/json')
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         relation = UserBookRelation.objects.get(user=self.user, book=self.book)
#         self.assertEqual(4, relation.rate)
#
#     def test_rate_wrong(self):
#         url = reverse('userbookrelation-detail', args=(self.book.id,))
#         self.client.force_login(self.user)
#         data = {
#             'rate': 6  # не входит в диапазон(1-5)
#         }
#         json_data = json.dumps(data)
#         response = self.client.patch(url, data=json_data,
#                                      content_type='application/json')
#         self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
