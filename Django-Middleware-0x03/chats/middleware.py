import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden



class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response  = get_response
        self.get_response = get_response
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler('requests.log', mode='a')
        self.form = "%(message)s"
        self.formatter = logging.Formatter(self.form)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start_time = datetime.strptime('21:00', '%H:%M').time()
        allowed_end_time = datetime.strptime('18:00', '%H:%M').time()

        if current_time < allowed_start_time and current_time > allowed_end_time:
            return HttpResponseForbidden(f"Access denied. The chat is only available between 9 PM and 6 PM.")

        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}
        self.time_window = timedelta(minutes=1)  # 1 minute time window

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = datetime.now()

            # Update message count for the IP address
            if ip_address in self.message_counts:
                last_message_time, count = self.message_counts[ip_address]
                if current_time - last_message_time < self.time_window:
                    if count >= 5:
                        return HttpResponseForbidden("You have exceeded the message limit. Please try again later.")
                    self.message_counts[ip_address] = (current_time, count + 1)
                else:
                    self.message_counts[ip_address] = (current_time, 1)
            else:
                self.message_counts[ip_address] = (current_time, 1)

        response = self.get_response(request)
        return response
    

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check the user's role
            if request.user.is_staff or request.user.is_superuser:
                # Allow access for admin or moderator
                return self.get_response(request)
            else:
                # Return 403 Forbidden for non-admin/moderator users
                return HttpResponseForbidden("You do not have permission to access this resource.")
        else:
            # Allow unauthenticated users to proceed
            return self.get_response(request)