from django.db.models import Q
from django.db import IntegrityError
from accounts.models import Account
from profiles.serializers import *
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import AllowOwner, AllowOwnerOrReadOnly
from rest_framework import views, viewsets, generics, status
from rest_framework.exceptions import NotFound


class AddDeviceRegistrationView(generics.RetrieveAPIView):
    """To Send User device gcm_registration_id or apns_token"""

    queryset = Account.objects.all()
    serializer_class = UserInfoSerializer

    def post(self, request, *args, **kwargs):
        pass

