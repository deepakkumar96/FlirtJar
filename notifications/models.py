from django.db import models
from flirtjarproject import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from push_notifications.models import Device

""""

class Device(models.Model):

    TYPE = (
        ('An', 'Android'),
        ('Ap', 'Apple')
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='device'
    )


class PushNotification(TimeStamp):
    pass

"""


class AndroidDevice(Device):
    registration_id = models.CharField(verbose_name=_("Registration ID"), max_length=200, unique=True)


class Notification(models.Model):
    MATCH = 'match'
    LIKE = 'like'
    CRUSH = 'crush'
    COINS = 'coins'
    VIEW = 'view'
    FJ = 'fj_team'
    GIFT = 'gift'

    NOTIFICATION_TYPE = (
        (MATCH, 'User Match'),
        (LIKE,  'Like'),
        (CRUSH, 'Crush or Superlike'),
        (COINS,  'Coins'),
        (VIEW,   'Profile View'),
        (FJ, 'FlirtJar Team'),
        (GIFT, 'Gift')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications'
    )
    notification_text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    # Notification-Type Related Info
    notification_type = models.CharField(choices=NOTIFICATION_TYPE, max_length=10, default=FJ)
    notification_icon = models.CharField(blank=True, null=True, max_length=255)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' : ' + self.notification_type


