from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    # url(r'^cards/$', views.AddDeviceRegistrationView.as_view(), name='device_registration'),
    url(r'^$', views.NotificationListView.as_view(), name='notification_list')
]