from django.db import models

from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'notification_text', 'timestamp', 'notification_type', 'notification_icon', 'is_seen')

