from django.db import models
from flirtjarproject import settings
from django.utils import timezone

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


class Notification(models.Model):
    MATCH = 'match'
    LIKE = 'like'
    CRUSH = 'crush'
    COINS = 'coins'
    VIEW = 'view'
    FJ = 'fj_team'

    NOTIFICATION_TYPE = (
        (MATCH, 'User Match'),
        (LIKE,  'Like'),
        (CRUSH, 'Crush or Superlike'),
        (COINS,  'Coins'),
        (VIEW,   'Profile View'),
        (FJ, 'FlirtJar Team')
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
