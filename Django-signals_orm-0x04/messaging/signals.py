# messaging/signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, skip
        return

    try:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance, old_content=original.content
            )
            instance.edited = True
    except Message.DoesNotExist:
        pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Messages sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Notifications
    Notification.objects.filter(user=instance).delete()

    # MessageHistory is deleted via CASCADE on Message
    # No need to delete it explicitly
