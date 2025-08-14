# chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed


def get_user_from_request(request):
    """
    Returns the authenticated user from the request.
    """
    if not request.user or not request.user.is_authenticated:
        raise AuthenticationFailed("User is not authenticated.")
    return request.user
