from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from notifications.models import Notification
from accounts.util import Device, get_user_device, DeviceNotFound


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_welcome_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            notification_text='Welcome To FlirtJar',
            notification_icon='http://127.0.0.1:8000/media/gifts/1.jpg'
        )


@receiver(post_save, sender=Notification)
def notify_user_for_notification_event(sender, instance=None, created=False, **kwargs):
    if created:
        print('sending notification')
        try:
            user_device = get_user_device(instance.user)
            user_device.send_push_notification(title=instance.notification_type,
                                               body=instance.notification_text,
                                               extra_data={
                                                   'type': instance.notification_type,
                                                   'user_to': str(instance.user)
                                               })
        except DeviceNotFound:
            print('users device does not exist.')
