### chats/permissions.py

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow access only to authenticated users.
    - Allow only participants of a conversation or related message
      to view, update, or delete the object.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Check for safe methods or modification permissions
        if request.method in permissions.SAFE_METHODS:
            pass  # Continue to check participant access
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            # Must also be a participant
            pass

        # For Conversation objects
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # For Message objects
        if hasattr(obj, "conversation") and hasattr(obj.conversation, "participants"):
            return request.user in obj.conversation.participants.all()

        return False
