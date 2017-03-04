from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from push_notifications.models import APNSDevice

from .models import Message


@receiver(post_save, sender=Message)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        user_device = instance.user_to.apnsdevice_set.first()
        if user_device:
            try:
                user_device.send_message('You have got new message')
            except:
                print('unable to send push notifications.')
