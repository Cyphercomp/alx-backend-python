from django.contrib.auth.models import AbstractUser     #Group, Permission
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    "email", "password", "user_id", "first_name", "last_name", "phone_number", "primary_key
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
        )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name="Email",
        help_text="Email address"  
    )
    password = models.CharField(
        max_length=255,
        unique=True
        )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=False
        )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
        )
    phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=True
        )
    #profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    

    # groups = models.ManyToManyField(
    #      Group,
    #      blank=True,
    #      verbose_name='groups',
    #      help_text='A user will get all permissions granted to each of their groups.',
    #      related_name="chats_user_groups",  # <--- Add this
    #      related_query_name="chats_user",
    #  )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     blank=True,
    #     verbose_name='user permissions',
    #     help_text='Specific permissions for this user.',
    #     related_name="chats_user_permissions",  # <--- Add this
    #     related_query_name="chats_user",
    # )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    # def get_profile_picture_url(self):
    #     """
    #     Returns the URL of the profile picture, or a default image if none is set.
    #     """
    #     if self.profile_picture:
    #         return self.profile_picture.url
    #     else:
    #         return 'static/images/default_profile.png'
            

    # def has_complete_profile(self):
    #     """
    #     Checks if the user has a complete profile (e.g., bio and location filled in).
    #     """
    #     return bool(self.bio and self.location)


# In models.py of another app (if you want to create a OneToOne relationship)
# from django.conf import settings
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     # ... other fields for the profile

class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False)
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        #help_text="Users participating in this conversation."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the conversation was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the conversation was last updated."
    )

    class Meta:
        ordering = ['-updated_at']
    def __str__(self):
        return f"Conversation between {self.participants.all()} with ID {self.conversation_id}"

class Message(models.Model):
    '''
    Represents a message within a conversation
    '''
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False
        )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to."
        )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent the message."
        )
    message_body= models.TextField(
        help_text="The content of the message."
        )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was sent."
        )

    class Meta:
        ordering = ['sent_at']
    def __str__(self):
        return f"Message {self.message_id} sent at {self.sent_at} with body: {self.message_body}"

