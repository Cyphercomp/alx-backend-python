from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipantOfConversation  # ✅ Import custom permission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # ✅ Apply permission
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def perform_create(self, serializer):
        # Automatically add the authenticated user to the conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def get_queryset(self):
        # ✅ Return only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'user added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter  # ✅
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    pagination_class = MessagePagination  # ✅

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

        if self.request.user not in conversation.participants.all():
            return Response({'detail': 'You are not a participant in this conversation.'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)