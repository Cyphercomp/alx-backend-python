from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantInConversation(permissions.BasePermission):
    """
    Permission to allow only participants in a conversation to send, view, update and delete messages.
    """
    def has_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        if view.action in  ["PUT", "PATCH", "DELETE"]:
            return (obj == request.user)
        else:
            return False 