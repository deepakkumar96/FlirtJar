from rest_framework import serializers
from rest_framework_gis.serializers  import GeoModelSerializer
from accounts.models import Account


class UserLocationSerializer(GeoModelSerializer):
    # location =
    class Meta:
        model = Account
        geo_field = 'location'
        fields = ('pk', 'first_name', 'last_name', 'profile_picture', 'location')
