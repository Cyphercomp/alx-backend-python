from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsOwner

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwner]  # Only owners can access their messages
