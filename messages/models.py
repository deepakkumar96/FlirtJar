from django.contrib.gis.db import models
from flirtjarproject import settings
from profiles.models import TimeStamp


""""
class GiftMessage(TimeStamp):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='gift_messages',
        related_query_name='gift_message'
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='gift_messages',
        related_query_name='gift_message'
    )


class Gift(models.Model):
    pass

"""



