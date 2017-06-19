from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account
from accounts.util import *
from django.urls import reverse
from rest_framework import status
from profiles.models import VirtualCurrency
from rest_framework.authtoken.models import Token


BASE_URL = 'localhost:8000/api'


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

