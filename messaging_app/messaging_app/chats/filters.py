from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import  filters
from .models import  Message
# from .serializers import Users, MessageSerializer, ConversationSerializer
# from typing import List, Dict, Any
# from rest_framework.response import Response

class MessageFilter(filters.Filterset):
    user = filters.ModelChoiceFilter(
        queryset = User.objects.all(),
        field_name = 'sender',
        label = 'Sender'
    )
    start_date = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label = 'StartDate_at')

    end_date = django_filters.DateTimeFilter(
    field_name='end_date',
    lookup_expr='lte',
    label = 'EndDate_at'
    )

class Meta:
        model = Message
        fields = ['user', 'start_date','end_date']