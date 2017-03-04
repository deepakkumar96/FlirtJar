from atk import relation_type_for_name
from django.contrib.gis.db import models
from flirtjarproject import settings
from profiles.models import TimeStamp


class Message(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_message',
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_message',
        on_delete=models.CASCADE
    )

    message_text = models.CharField(max_length=400, null=True)
    sent_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_from) + ' => ' + str(self.user_to) + ' : ' + self.message_text

