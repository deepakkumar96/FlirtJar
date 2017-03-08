from django.contrib import admin
from notifications.models import Notification, AndroidDevice

admin.site.register(Notification)
admin.site.register(AndroidDevice)
