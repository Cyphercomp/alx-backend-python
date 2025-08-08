from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Conversation, Message

User = get_user_model()  # or Important: Use get_user_model()

#["serializers.SerializerMethodField()", "serializers.ValidationError"]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'phone_number', 'password', 'last_name')
        read_only_fields = ('user_id',)  # Prevent ID modification


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User serializer
    # conversation = serializers.PrimaryKeyRelatedField(read_only=True) #Or StringRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = ('conversation', 'sender', 'message_body', 'send_at')
        read_only_fields = ('message_id', 'sender', 'send_at') #timestamp is often set automatically


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested User serializer
    messages = MessageSerializer(many=True, read_only=True)  # Nested Message serializer

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'messages', 'created_at', 'updated_at')
        read_only_fields = ('conversation_id', 'created_at', 'updated_at')


#Serializers for creating conversations and Messages

class CreateConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Conversation
        fields = ('participants',)

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class CreateMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True) #added to ensure text is a required field

    class Meta:
        model = Message
        fields = '__all__'