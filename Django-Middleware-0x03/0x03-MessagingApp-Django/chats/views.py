### chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle creating, listing, retrieving, updating,
    and deleting conversations for authenticated users.
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        """Return only conversations the authenticated user participates in."""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create a conversation and add the authenticated user as a participant."""
        participant_ids = self.request.data.get("participants", [])
        if not participant_ids:
            raise PermissionDenied("Participants are required.")

        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            raise PermissionDenied("No valid participants found.")

        conversation = serializer.save()
        conversation.participants.add(self.request.user, *participants)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle sending, retrieving, and filtering messages
    in conversations for authenticated and authorized users.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["message_body"]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        """Return messages only for conversations the user participates in."""
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=self.request.user,
            )
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Send a message only if the user is a participant of the conversation."""
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation.")
        serializer.save(sender=self.request.user)


# # chats/views.py

# from rest_framework import viewsets, filters
# from rest_framework import viewsets, status, filters
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Message, Conversation, CustomUser
# from .serializers import MessageSerializer, ConversationSerializer
# from .serializers import ConversationSerializer, MessageSerializer
# from .permissions import IsParticipantOfConversation
# from .filters import MessageFilter
# from django.shortcuts import get_object_or_404


# class ConversationViewSet(viewsets.ModelViewSet):
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated, IsParticipantOfConversation]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ["created_at"]

#     def get_queryset(self):
#         return Conversation.objects.filter(participants=self.request.user)

#     def perform_create(self, serializer):
#         participant_ids = self.request.data.get("participants", [])
#         if not participant_ids:
#             raise PermissionDenied("Participants are required.")

#         participants = CustomUser.objects.filter(user_id__in=participant_ids)
#         if not participants.exists():
#             raise PermissionDenied("No valid participants found.")

#         conversation = serializer.save()
#         conversation.participants.add(self.request.user, *participants)
#         conversation.save()


# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated, IsParticipantOfConversation]
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ["message_body"]
#     filterset_class = MessageFilter

#     def get_queryset(self):
#         return Message.objects.filter(conversation__participants=self.request.user)

#     def perform_create(self, serializer):
#         conversation = serializer.validated_data["conversation"]
#         if self.request.user not in conversation.participants.all():
#             raise PermissionDenied("You are not part of this conversation.")
#         serializer.save(sender=self.request.user)
