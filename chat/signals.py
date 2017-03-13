from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from push_notifications.models import APNSDevice

from .models import Message


@receiver(post_save, sender=Message)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # finding users device in APNS
        user_device = instance.user_to.apnsdevice_set.first()

        # finding users device in Android
        if not user_device:
            user_device = instance.user_to.androiddevice_set.first()

        if user_device:
            # sending a push notification to receiver of chat message if user device exist
            try:
                print('sending android push')
                user_device.send_message(message_title='Chat Message',
                                         message_body='You have got new message from ' + str(instance.user_from),
                                         data_message={
                                             'type': 'chat',
                                             'user_from': str(instance.user_from),
                                             'user_to': str(instance.user_to)
                                         })

            except:
                print('unable to send push notifications. to ', user_device)
        else:
            print('No device found for ', instance.user_to)
