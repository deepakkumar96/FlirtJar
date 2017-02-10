from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from accounts.serializers import UserSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from profiles.serializers import *


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        print('query')
        return Notification.objects.filter(user=self.request.user, is_seen=False)

    def get(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        serializers_data = NotificationSerializer(notifications, many=True).data
        notifications.update(is_seen=True)  # updating seen notifications
        return Response(serializers_data)


class AddDeviceRegistrationView(generics.RetrieveAPIView):
    """To Send User device gcm_registration_id or apns_token"""

    queryset = Account.objects.all()
    serializer_class = UserInfoSerializer

    def post(self, request, *args, **kwargs):
        pass

