from django.shortcuts import redirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Request path: {request.path}, User authenticated: {request.user.is_authenticated}")
        if request.path == '/' and not request.user.is_authenticated:
            logger.debug("Redirecting to login URL")
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        logger.debug(f"Response status code: {response.status_code}")
        return response