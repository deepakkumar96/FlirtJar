from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import VirtualCurrency, UserGifts
from notifications.models import Notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        VirtualCurrency.objects.create(user=instance)


@receiver(post_save, sender=UserGifts)
def create_notification_on_sending_gift(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user_to,
            notification_type=Notification.GIFT,
            notification_text=str(instance.user_from) + ' sent you a gift.',
            notification_icon='fjhf',
        )
