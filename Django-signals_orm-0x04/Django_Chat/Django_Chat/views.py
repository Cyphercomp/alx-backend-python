from django.shortcuts import render
from .models import Message
from django.contrib.auth.models import User

def conversation_view(request, user_id):
    user1 = request.user
    user2 = User.objects.get(id=user_id)

    # Optimized query
    messages = Message.objects.filter(
        sender=user1, receiver=user2
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

    context = {'messages': messages}
    return render(request, 'conversation.html', context)

def get_threaded_replies(message):
    thread = []
    replies = message.replies.all()

    for reply in replies:
        nested = get_threaded_replies(reply)
        thread.append({
            'message': reply,
            'replies': nested
        })

    return thread

# Fetch top-level messages (those without a parent)
top_level_messages = Message.objects.filter(
    sender=user1, receiver=user2, parent_message=None
).select_related('sender', 'receiver').prefetch_related('replies')

threaded_conversations = []
for message in top_level_messages:
    threaded_conversations.append({
        'message': message,
        'replies': get_threaded_replies(message)
    })

context = {'threaded_conversations': threaded_conversations}
return render(request, 'conversation.html', context)
