# from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Message, Conversation, User

# User = get_user_model()  # or Important: Use get_user_model()

#["serializers.SerializerMethodField()", "serializers.ValidationError"]

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'phone_number', 'password', 'last_name')
        read_only_fields = ('user_id',)  # Prevent ID modification


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_id = serializers.UUIDField(read_only=True)
    message_body = serializers.CharField(max_length=500)
    sent_at = serializers.DateTimeField(read_only=True)
    message_preview = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ('message_id','conversation', 'sender', 'message_body', 'sent_at','message_preview')
        read_only_fields = ('message_id', 'sender', 'sent_at','message_preview') #send_a is often set automatically
    def get_message_preview(self, obj):
        return obj.all()

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

    # def create(self, validated_data):
    #     participants = validated_data.pop('participants')
    #     conversation = Conversation.objects.create(**validated_data)
    #     conversation.participants.set(participants)
    #     conversation.save()
    #     return conversation


class CreateMessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(required=True, help_text="The content of the message.") #added to ensure text is a required field

    class Meta:
        model = Message
        fields = '__all__'