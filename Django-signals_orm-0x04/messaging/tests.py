from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='test123')
        self.user2 = User.objects.create_user(username='bob', password='test123')

    def test_notification_created_on_new_message(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob!")

        notifications = Notification.objects.filter(user=self.user2)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, message)
