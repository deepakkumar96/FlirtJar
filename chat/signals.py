from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from push_notifications.models import APNSDevice

from .models import Message


@receiver(post_save, sender=Message)
def send_notification_on_message(sender, instance=None, created=False, **kwargs):
    if created:
        # finding users device in APNS
        """
        user_device = instance.user_to.apnsdevice_set.first()
        if user_device:
            try:
                print('sending apns push : ', type(user_device))
                user_device.send_message(
                    message={
                        'title': instance.user_from.get_short_name(),
                        'body': instance.message_text
                    },
                    extra={
                        'type': 'chat',
                        'user_from': str(instance.user_from),
                        'user_to': str(instance.user_to)
                    }
                )
                print('apns sent')
            except:
                print('unable to send apns push notifications. to ', user_device)

        # finding users device in Android
        elif not user_device:"""

        # Sending notification to user device using FCM
        user_device = instance.user_to.androiddevice_set.first()

        if user_device:
            # sending a android push notification to receiver of chat message if user device exist
            try:
                print('sending android push')
                user_device.send_message(message_title=instance.user_from.get_short_name(),
                                         message_body=instance.message_text,
                                         data_message={
                                                 'type': 'chat',
                                                 'user_from': str(instance.user_from),
                                                 'user_to': str(instance.user_to)
                                         })
            except:
                print('unable to send push notifications. to ', user_device)
        else:
            print('No device found for ', instance.user_to)
