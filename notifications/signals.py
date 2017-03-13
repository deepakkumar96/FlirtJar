from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from notifications.models import Notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_welcome_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            notification_text='Welcome To FlirtJar',
            notification_icon='http://127.0.0.1:8000/media/gifts/1.jpg'
        )
