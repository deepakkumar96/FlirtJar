from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from push_notifications.models import GCMDevice

from chat.models import Message
from chat.serializers import MessageReceiveSerializer, MessageSendSerializer
from accounts.models import Account
from chat.api.util import get_all_messages


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSendSerializer
    queryset = Message.objects.all()

    def list(self, request, *args, **kwargs):
        user_from = request.query_params.get('user_from', None)
        if user_from:

            try:
                user_from = Account.objects.get(pk=user_from)
                print(user_from)
                new_messages = get_all_messages(user_from=user_from, user_to=request.user) # Message.objects.filter(user_to=request.user, user_from=user_from, is_seen=False)[:25]
            except Account.DoesNotExist:
                raise NotFound('user_from is invalid user id.')

            serializer = MessageReceiveSerializer(new_messages, many=True).data
            # new_messages.delete() del
            return Response(serializer)
        else:
            return Response([])

