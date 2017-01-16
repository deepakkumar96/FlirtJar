from django.contrib.gis.db import models
from flirtjarproject import settings
from profiles.models import TimeStamp

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
