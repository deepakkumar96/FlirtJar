from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    # url(r'^locations$', views.UserListView.as_view(), name='user_list_view'),
    url(r'^$', views.MessageListView.as_view(), name='message_list'),
    url(r'^user/(?P<user>[0-9]+)/delete-chat$', views.DeleteChatHistoryView.as_view(), name='delete_chat_history'),
]