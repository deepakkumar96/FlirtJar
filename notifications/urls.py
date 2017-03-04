from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    # url(r'^cards/$', views.AddDeviceRegistrationView.as_view(), name='device_registration'),
    url(r'^$', views.NotificationListView.as_view(), name='notification_list'),
    url(r'^(?P<noti_id>[0-9]+)/markread/$', views.NotificationToggleView.as_view(), name='notification_toggle'),
    url(r'device/$', views.AddDeviceRegistrationView.as_view(), name='device_registration'),
]