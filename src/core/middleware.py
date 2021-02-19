from django.contrib.auth.models import AnonymousUser

from django.utils import timezone


class UpdateUserLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and not isinstance(request.user, AnonymousUser):
            user = request.user
            user.last_request = timezone.now()
            user.save()
        response = self.get_response(request)
        return response
