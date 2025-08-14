# chats/models.py

import os
import logging
from datetime import datetime
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
import time
from collections import defaultdict
from django.http import JsonResponse

# Log file path (inside your Django project root directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "requests.log")

# Ensure logger is configured only once
logger = logging.getLogger("request_logger")
if not logger.hasHandlers():
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = (
            request.user
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )
        message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        print("Server time:", datetime.now())

        # Allow access ONLY between 18:00 and 21:00
        if not (now.hour >= 18 and now.hour < 21):
            return HttpResponseForbidden(
                "Access to the chat is restricted at this time."
            )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logs = defaultdict(list)  # {ip: [datetime objects]}

    def __call__(self, request):
        # Limit only POST requests to /api/conversations/<uuid>/messages/
        if request.method == "POST" and "/messages/" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            self.request_logs[ip] = [
                timestamp
                for timestamp in self.request_logs[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            print(
                f"[DEBUG] IP {ip} has sent {len(self.request_logs[ip])} messages in the last 60 seconds."
            )

            # Check if IP exceeded the 5 message limit
            if len(self.request_logs[ip]) >= 5:
                return JsonResponse(
                    {"error": "Too many messages. Please wait a minute."}, status=403
                )

            # Log this new request
            self.request_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define a list of endpoints that require admin access
        self.restricted_paths = [
            "/api/conversations/",
        ]

    def __call__(self, request):
        # Allow access to admin and token endpoints without restriction
        if request.path.startswith("/admin/") or request.path.startswith("/api/token/"):
            return self.get_response(request)

        user = request.user
        if any(request.path.startswith(path) for path in self.restricted_paths):
            if user.is_authenticated:
                # Check if the user is staff (admin access)
                if not (user.is_staff or user.is_superuser):
                    # if not user.is_staff:
                    return JsonResponse(
                        {"error": "Permission denied. Admins only."},
                        status=403,
                    )
            else:
                return JsonResponse({"error": "Authentication required."}, status=401)

        return self.get_response(request)
