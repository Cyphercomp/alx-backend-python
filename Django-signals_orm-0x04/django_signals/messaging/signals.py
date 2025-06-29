from .models import Message , Notification
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def create_notification(sender,instance,created,*args,**kwargs):
    if created :
        Notification.objects.create(user = instance.receiver , message= instance)

    