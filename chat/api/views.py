from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from push_notifications.models import GCMDevice

from chat.models import Message
from chat.serializers import MessageSerializer
from accounts.models import Account


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        print('Hello')

    def list(self, request, *args, **kwargs):
        user_from = request.query_params.get('user_from', None)
        if user_from:

            try:
                user_from = Account.objects.get(pk=user_from)
                print(user_from)
                new_messages = Message.objects.filter(user_to=request.user, user_from=user_from, is_seen=False)
            except Account.DoesNotExist:
                raise NotFound('user_from is invalid user id.')

            serializer = MessageSerializer(new_messages, many=True).data
            new_messages.delete()
            return Response(serializer)
        else:
            return Response([])

