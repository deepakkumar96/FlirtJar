from django.conf.urls import url, include
from django.contrib import admin
from .api import views

urlpatterns = [
    # url(r'^locations$', views.UserListView.as_view(), name='user_list_view'),
    url(r'^custom/nearby/(?P<near_by>[0-9]+)/(?P<unit>[A-Za-z]+)/$',
        views.NearByCustomLatLong.as_view(),
        name='nearby_custom_lat_long'),

    url(r'^nearby/(?P<near_by>[0-9]+)/(?P<unit>[A-Za-z]+)/$', views.NearByLocationUsers.as_view(), name='nearbylocation'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserLocationDetail.as_view(), name='user_detail_view'),
    url(r'^user/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserLocationDetailByEmail.as_view(), name='user_detail_view'),
]
