from django.test import TestCase

from accounts.models import Account
from accounts.util import *

# Create your tests here.


class DeviceTest(TestCase):

    def test_get_user_device(self):

        user = Account.objects.get(pk=1)
        device = get_user_device(user)

        self.assertEqual(device.device_type, Device.IOS, 'same device type')
