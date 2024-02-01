from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from archive.models import Dossier, ArchiveBox, Sector
from bank_clients.models import Contract, Product, Client

User = get_user_model()


class DossierCheckViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
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

        # Set up the API URL for the DossierCheckView


    def test_retrieve_dossier(self):
        url = reverse('dossierchecking-detail', kwargs={'pk': self.dossier.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on your expected behavior

    def test_update_dossier(self):
        data = {
            # Add data for updating the Dossier
            # ...
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on your expected behavior

    def test_invalid_barcode_retrieve(self):
        invalid_barcode_url = reverse('dossierchecking-detail', kwargs={'barcode': 'invalid-barcode'})
        response = self.client.get(invalid_barcode_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Add more assertions based on your expected behavior for an invalid barcode

    def test_invalid_barcode_update(self):
        invalid_barcode_url = reverse('dossierchecking-detail', kwargs={'barcode': 'invalid-barcode'})
        data = {
            # Add data for updating the Dossier
            # ...
        }
        response = self.client.patch(invalid_barcode_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Add more assertions based on your expected behavior for an invalid barcode

    # Add more test cases based on your requirements
