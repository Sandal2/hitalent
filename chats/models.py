from django.core.validators import MaxLengthValidator
from django.db import models


class Chat(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(validators=[MaxLengthValidator(5000)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message ID: {self.pk} | Message Text: {self.text[:20]}'

    class Meta:
        ordering = ['-created_at']
