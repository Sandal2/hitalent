from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from chats.models import Chat, Message
from chats.serializers import ChatCreateSerializer, MessageCreateSerializer, ChatDetailSerializer


class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatCreateSerializer


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])
        serializer.save(chat=chat)


class ChatRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            limit = int(self.request.query_params.get('limit', 20))

        except ValueError:
            limit = 20

        context['limit'] = min(limit, 100)

        return context
