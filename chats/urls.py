from django.urls import path

from chats.views import ChatCreateView, SendMessageView, ChatRetrieveDestroyView

app_name = 'chats'

urlpatterns = [
    path('', ChatCreateView.as_view(), name='create-chat'),
    path('<int:pk>/messages/', SendMessageView.as_view(), name='send-message'),
    path('<int:pk>/', ChatRetrieveDestroyView.as_view(), name='chat-detail')
]
