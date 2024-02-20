import json

from django.contrib.auth import get_user_model

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models.users import AMSGroup
from archive.models import ArchiveBox, Dossier, Sector
from bank_clients.models import Client, Product, Contract

User = get_user_model()


class RegistrationTestCase(APITestCase):
    """Тестирование CRUD"""

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.registration_group = AMSGroup.objects.create(name='Регистраторы')
        self.user.groups.add(self.registration_group)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
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
        response = self.client.post(url, data=json_data, content_type='application/json')
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
