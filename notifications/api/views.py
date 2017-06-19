from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from push_notifications.models import APNSDevice, GCMDevice

from accounts.serializers import UserSerializer
from notifications.models import Notification, AndroidDevice
from notifications.serializers import NotificationSerializer
from profiles.serializers import *
from .util import DeviceType


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
        return Notification.objects.filter(user=self.request.user, is_seen=False)

    def get(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        serializers_data = NotificationSerializer(notifications, many=True)
        # notifications.update(is_seen=True)  # updating seen notifications
        return Response(serializers_data.data)


class NotificationToggleView(generics.UpdateAPIView):
    """
        Mark a notification as read.
        and after marking this notification wont be visible in notification list.

        It accepts id of the notification in the URL.
    """
    serializer_class = NotificationSerializer
    lookup_url_kwarg = 'noti_id'

    def update(self, request, *args, **kwargs):

        try:
            print(self.lookup_url_kwarg)
            notification = Notification.objects.get(pk=kwargs['noti_id'])
        except Notification.DoesNotExist:
            raise NotFound({'detail': 'notification not found with given id.'})

        notification.is_seen = True
        notification.save()
        return Response(self.get_serializer(notification).data)


class AddDeviceRegistrationView(views.APIView):
    """
    To register device token(cm_registration_id or apns_token).
    * `Request - `
        <pre>
            POST /api/notification/device/
         {
        "registration_id": "054c7c42d7316d9ab30e8d5d328263038f3963c326d19e3d6f6ba48c839ae98f",
        "device_type": "ios"
         }
        </pre>`
    """

    def post(self, request, *args, **kwargs):
        device_type = request.data.get('device_type', None)
        registration_id = request.data.get('registration_id', None)

        if (not device_type) or (not registration_id):
            raise NotFound('either registration_id or device is missing.')

        device = DeviceType.get_device_type(device_type)  # Getting device type from request

        # Checking whether device already exist for user or not
        user_device = None
        if device == DeviceType.IOS:
            try:
                user_device = APNSDevice.objects.get(user=request.user)  # checking device for requested user in IOS
            except APNSDevice.DoesNotExist:
                pass

        elif device == DeviceType.ANDROID:
            try:
                user_device = AndroidDevice.objects.get(user=request.user) # checking device for requested user in Android
            except AndroidDevice.DoesNotExist:
                pass

        if not user_device:  # if requested user's device does not exist, then creating device for the user.
            if device == DeviceType.IOS:
                user_device = APNSDevice.objects.create(
                    registration_id=registration_id,
                    user=request.user,
                    name=DeviceType.IOS
                )

            elif device == DeviceType.ANDROID:
                user_device = AndroidDevice.objects.create(
                    registration_id=registration_id,
                    user=request.user,
                    name=DeviceType.ANDROID
                )
            else:
                raise NotFound('device type is unknown.')
        else:  # if user's deice exist and need to update its device_token
            if device:
                print('UPDATING')
                user_device.registration_id = registration_id
                user_device.name = device_type
                user_device.save()

        return Response(
            {
                'registration_id': user_device.registration_id,
                'device_type': user_device.name
            }
        )
