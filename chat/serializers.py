from rest_framework import serializers

from .models import Message
from accounts.models import Account


class AccountNamePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'profile_picture')


class MessageSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('is_seen', 'read_at')


class MessageReceiveSerializer(serializers.ModelSerializer):
    user_from = AccountNamePictureSerializer(read_only=True)
    user_to = AccountNamePictureSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ('is_seen', 'read_at')



