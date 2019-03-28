from django.test import TestCase, tag
from unittest import skip
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import Account
from profiles.models import *
from notifications.models import *
from accounts.util import *
from django.urls import reverse
from rest_framework import status
from profiles.models import VirtualCurrency
from rest_framework.authtoken.models import Token
from django.db import transaction


BASE_URL = 'localhost:8000/api'


class UserListViewApiTest(APITestCase):
    

    def create_accounts(self):

        def crt(id, pk): return Account.objects.create(oauth_id=id, pk=pk)

        return  [
            crt('Deepak', 1),
            crt('Jerin', 2),
            crt('Mrinal', 3),
            crt('Harsh', 4),
            crt('Vikas', 5),
            crt('Hari', 6),
            crt('Dishant', 7)
        ]

    def setUp(self):
        self.accounts = self.create_accounts()
        self.url = reverse('user_list_view')
        
        self.data = [
                {
                   "user_from" : 1,
                    "user_to":    2,
                    "response": 0
                },
                {
                    "user_from" : 2,
                    "user_to":    1,
                    "response": 2
                }
        ]

        # tuning-off auth-system
      

    @skip('skipped')
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


    def test_a_user_response_to_profile(self):
        with transaction.atomic():
            self.data = [
                    {
                       "user_from" : 1,
                        "user_to":    2,
                        "response": 0
                    },
                    {
                        "user_from" : 2,
                        "user_to":    1,
                        "response": 2
                    },
                    {
                       "user_from" : 1,
                        "user_to":    2,
                        "response": 0
                    },
                    {
                        "user_from" : 2,
                        "user_to":    1,
                        "response": 1
                    }
            ]

            self.url = '/api/profile/view/user/1/'
            token = Token.objects.get(user=Account.objects.get(pk=1))
            
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response1 = client.post(self.url, self.data, format='json')

            self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response1.data, {"detail": "data saved."})

            self.assertEqual(ProfileView.objects.count(), 2)
            self.assertEqual(UserMatch.objects.count(), 1)

            deepak = Account.objects.get(pk=1)
            jerin = Account.objects.get(pk=2)

            self.assertEqual(deepak.likes, 0)
            self.assertEqual(deepak.skipped, 0)
            self.assertEqual(deepak.superlikes, 1)

            self.assertEqual(jerin.likes, 1)
            self.assertEqual(jerin.skipped, 0)
            self.assertEqual(jerin.superlikes, 0)
            
            # testing created notifications
            self.assertEqual(Notification.objects.count(), len(self.accounts)+4)
            notifications = Notification.objects.all()
            #self.assertTrue(notifications[0].user == jerin)
            #self.assertTrue(notifications[1].user == deepak)
            match1 = UserMatch.objects.get(pk=1)
            print('views : ', ProfileView.objects.all())
