from rest_framework import serializers

from chats.models import Chat, Message


class ChatCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Chat
        fields = ['title']


class MessageCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=5000, allow_blank=False)

    class Meta:
        model = Message
        fields = ['text']


class MessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at']


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'title', 'messages', 'created_at']

    def get_messages(self, obj):
        limit = self.context.get('limit', 20)
        qs = obj.messages.order_by('-created_at')[:limit]

        return MessageReadSerializer(qs, many=True).data
