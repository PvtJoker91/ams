import json

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models.users import AMSGroup
from archive.models import Dossier, ArchiveBox, Sector
from bank_clients.models import Contract, Product, Client

User = get_user_model()


class DossierCheckViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test_user_password')
        self.logistics_group = AMSGroup.objects.create(name='Логисты')
        self.user.groups.add(self.logistics_group)
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

        self.dossier_data = {
            'barcode': 'D00-00-00000001',
            'status': 'Under checking',
            'current_sector': self.sector,
            'contract': self.contract,
            'archive_box': self.archive_box1,
            'registerer': self.user
        }

        self.dossier1 = Dossier.objects.create(**self.dossier_data)


    def test_update_dossier(self):
        url = f'/api/logistics/checking-dossier/{self.dossier1.pk}/'
        data = {
            'barcode': self.dossier1.pk,
            'status': 'Is checked',
            'archive_box': self.archive_box2.id,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Is checked')


    def test_invalid_barcode_update(self):
        url = f'/api/logistics/checking-dossier/D00-00-00000002/'
        data = {
            'barcode': 'D00-00-00000002',
            'status': 'Is checked',
            'archive_box': self.archive_box2.id,
        }
        response = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

