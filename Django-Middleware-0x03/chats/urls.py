from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats import views

routers = DefaultRouter()
routers.register(r'conversations', views.ConversationViewSet, basename='conversation')
routers.register(r'messages', views.MessageViewSet, basename='message')
#["NestedDefaultRouter"]
#["routers.DefaultRouter()"]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(routers.urls)),
    path('api-auth/',include('rest_framework.urls'))
]