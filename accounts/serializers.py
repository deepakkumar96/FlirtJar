from rest_framework import serializers
from rest_framework_gis.serializers  import GeoModelSerializer
from .models import Account


class UserSerializer(GeoModelSerializer):
    email = serializers.EmailField(required=False)
    # oauth_id = serializers.CharField(required=False)
    rating = serializers.ReadOnlyField(source='score')
    language = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                     child=serializers.CharField(max_length=32, allow_blank=True))
    tags = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                 child=serializers.CharField(max_length=32, allow_blank=True))

    class Meta:
        model = Account
        geo_field = 'location'
        exclude = ('is_admin', 'is_active', 'password', 'oauth_id', 'email')
        extra_kwargs = {
            'oauth_id': {'write_only': True}
        }


class UserRegisterSerializer(GeoModelSerializer):
    email = serializers.EmailField(required=False)
    # oauth_id = serializers.CharField(required=False)
    rating = serializers.ReadOnlyField(source='score')
    language = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                     child=serializers.CharField(max_length=32, allow_blank=True))
    tags = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                 child=serializers.CharField(max_length=32, allow_blank=True))

    class Meta:
        model = Account
        geo_field = 'location'
        exclude = ('is_admin', 'is_active', 'password', 'email')
        extra_kwargs = {
            'oauth_id': {'write_only': True}
        }


class UserSerializerWithoutOAuthId(GeoModelSerializer):
    rating = serializers.ReadOnlyField(source='score')
    language = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                     child=serializers.CharField(max_length=32, allow_blank=True))
    tags = serializers.ListField(allow_empty=True, allow_null=True, required=False,
                                 child=serializers.CharField(max_length=32, allow_blank=True))

    class Meta:
        model = Account
        geo_field = 'location'
        exclude = ('is_admin', 'is_active', 'password', 'oauth_id')

