import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This model includes additional fields for user profiles and messaging features.
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    A conversation can have multiple participants and contains messages exchanged between them.
    """

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"Conversation {self.conversation_id}"
        return f"Conversation {self.conversation_id} between {[user.username for user in self.participants.all()]}"


class Message(models.Model):
    """
    Model representing a message sent in a conversation.
    Each message is linked to a sender and a conversation, and contains the text of the message.
    """

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:30]}..."
