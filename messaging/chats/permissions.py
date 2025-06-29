from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users who are participants of the conversation
    to read/write/update/delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', obj)

        if request.method in SAFE_METHODS:
            # GET, HEAD, OPTIONS: allow if user is participant
            return request.user in conversation.participants.all()

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Allow only if user is a participant
            return request.user in conversation.participants.all()

        return False
