from django.shortcuts import redirect


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path == '/login/' and not request.path == '/registration/' and not request.path == '/':
            return redirect('login')
        return self.get_response(request)
