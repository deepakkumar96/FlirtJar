from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account
from accounts.util import *
from django.urls import reverse
from rest_framework import status
from profiles.models import VirtualCurrency
from rest_framework.authtoken.models import Token

# Create your tests here.

BASE_URL = 'localhost:8000/api'

"""
class DeviceTest(TestCase):

    def test_get_user_device(self):

        user = Account.objects.get(pk=1)
        device = get_user_device(user)

        self.assertEqual(device.device_type, Device.IOS, 'same device type')
"""


class AccountModelTest(TestCase):
    pass


class UserListViewApiTest(APITestCase):
    def test_create_account(self):
        url = reverse('user_list_view')
        data = {
            'oauth_id': 'test1',
            'first_name': 'Test_1'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)

        created_account = Account.objects.get(pk=1)

        self.assertEqual(created_account.first_name, 'Test_1')

        user_currency = VirtualCurrency.objects.get(user=created_account)

        self.assertEqual(user_currency.coins, 2)
        self.assertEqual(user_currency.user, created_account)

        created_token = Token.objects.get(user=created_account)
        self.assertEqual(created_token.key, response.data['Token'])

        # Signing-In again with the same credentials
        response2 = self.client.post(url, {'oauth_id': data['oauth_id']}, format='json')

        self.assertEqual(response.data, response2.data)
