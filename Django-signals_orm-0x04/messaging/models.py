# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    read = models.BooleanField(default=False)
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages",
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit History of Message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about message from {self.message.sender}"
