from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Chats app API URLs under /api/chats/
    path('api/chats/', include('chats.urls')),

    # Optionally keep DRF's browsable API login URLs
    path('api-auth/', include('rest_framework.urls')),
]
