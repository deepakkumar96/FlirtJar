from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list_view'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail_view'),
    url(r'^me/$', views.CurrentUserDetail.as_view(), name='current_user'),
]