from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from accounts.serializers import UserSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from profiles.serializers import *


class NotificationListView(generics.ListAPIView):
    """
    Notification API:

	/api/notifications

	This return a list of all the new notification and after returning notification server also delete the returned notifications, so you wont get
	the same notifications again and again.

	Content of notification is:

	1. notification_text
	2. timestamp : date and time
	3. notification_type : type of notification it can be MATCH, CRUSH, FJ_Team
	4. notification_icon: icon of the notification

    """
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

