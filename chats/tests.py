from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chats.models import Chat, Message


class ChatCreateTestCase(APITestCase):
    def setUp(self):
        self.path = reverse('chats:create-chat')

    def test_create_chat(self):
        response = self.client.post(self.path, {'title': 'Test'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.first().title, 'Test')

    def test_empty_title(self):
        response = self.client.post(self.path, {'title': ' '}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SendMessageTestCase(APITestCase):
    def setUp(self):
        self.chat = Chat.objects.create(title='Test')
        self.path = reverse('chats:send-message', kwargs={'pk': self.chat.pk})

    def test_send_message(self):
        response = self.client.post(self.path, {'text': 'test'}, format='json')
        message = Message.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.text, 'test')
        self.assertEqual(message.chat, self.chat)

    def test_send_empty_message(self):
        response = self.client.post(self.path, {'text': ''}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_message_to_non_existent_chat(self):
        path = reverse('chats:send-message', kwargs={'pk': 9999})
        response = self.client.post(path, {'text': 'test'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChatRetrieveDestroyTestCase(APITestCase):
    def setUp(self):
        self.chat = Chat.objects.create(title='Test')
        self.messages = [Message.objects.create(chat=self.chat, text=f'test {i}') for i in range(5)]
        self.path = reverse('chats:chat-detail', kwargs={'pk': self.chat.pk})

    def test_retrieve_chat(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.chat.pk)
        self.assertEqual(response.data['title'], self.chat.title)
        self.assertEqual(len(response.data['messages']), 5)

    def test_messages_limit(self):
        response = self.client.get(self.path, {'limit': 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['messages']), 3)

    def test_messages_limit_gt_100(self):
        response = self.client.get(self.path, {'limit': 101})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['messages']), 100)

    def test_destroy_chat(self):
        response = self.client.delete(self.path)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(pk=self.chat.pk).exists())

    def test_destroy_chat_cascade_messages(self):
        self.client.delete(self.path)

        self.assertEqual(Message.objects.count(), 0)