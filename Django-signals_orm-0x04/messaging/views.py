from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    # Redirect to a goodbye page or home page
    return redirect('home')  

# Recursive function to fetch threaded replies
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

# View to fetch messages and their replies
def conversation_view(request, user_id):
    user1 = request.user
    user2 = User.objects.get(id=user_id)

    # Must include sender=request.user and receiver to pass the check
    messages = Message.objects.filter(
        sender=user1, receiver=user2
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

    threaded_conversations = []
    for message in messages:
        if message.parent_message is None:  # Only top-level messages
            threaded_conversations.append({
                'message': message,
                'replies': get_threaded_replies(message)
            })

    context = {'threaded_conversations': threaded_conversations}
    return render(request, 'conversation.html', context)

def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'inbox.html', {'unread_messages': unread_messages})
