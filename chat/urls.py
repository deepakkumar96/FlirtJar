from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    # url(r'^locations$', views.UserListView.as_view(), name='user_list_view'),
    url(r'^$', views.MessageListView.as_view(), name='message_list'),
]