# In your_app/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import LoginHistory

class LoginHistoryMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated and request.path == '/login/':
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            LoginHistory.objects.create(user=request.user, ip_address=ip_address, user_agent=user_agent)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ActiveSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        request.session.modified = True
        return response
