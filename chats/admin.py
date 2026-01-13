from django.contrib import admin

from chats.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id', 'title']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id', 'chat__title', 'text']
    readonly_fields = ['created_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['chat']
        return self.readonly_fields
