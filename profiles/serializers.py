from rest_framework import serializers
from .models import Rating, ProfileView, UserMatch, VirtualCurrency, Gift, UserGifts
from accounts.models import Account
from accounts.serializers import UserSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'first_name', 'last_name', 'profile_picture', 'location', 'status')


class UserRatingSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField(source='score')

    class Meta:
        model = Account
        fields = ('pk', 'likes', 'skipped', 'superlikes', 'rating')


class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('pk', 'likes', 'superlikes', 'skipped')


class UserProfileResponseSerializer(serializers.ModelSerializer):
    user_from = UserInfoSerializer(read_only=True)

    class Meta:
        model = ProfileView
        fields = ('user_from',)


class UserMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatch
        fields = ('user_from', 'user_to')


class UserProfileMatchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileView
        fields = '__all__'


class VirtualCurrencySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VirtualCurrency
        fields = ('user', 'coins')


class VirtialCurrencyOperation(serializers.Serializer):
    operation = serializers.CharField(max_length=10)
    coins = serializers.IntegerField()


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'


class UserGiftSerializer(serializers.ModelSerializer):
    gift = GiftSerializer()

    class Meta:
        model = UserGifts
        fields = ('id', 'user_from', 'user_to', 'gift',)


class GiftSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGifts
        fields = ('user_from', 'user_to', 'gift')

