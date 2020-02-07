from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import translation


class TryAuthenticateMiddleware:
    def __init__(self, get_response):
        self.OIDC_TRY_AUTH_URL = reverse('oidc_try_authenticate')
        self.OIDC_CALLBACK_URL = reverse('oidc_authentication_callback')
        self.OIDC_LOGOUT = reverse('oidc_logout')
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and 'oidc_attempted' not in request.session:
            if self.OIDC_TRY_AUTH_URL in request.path or self.OIDC_CALLBACK_URL in request.path:
                return HttpResponse("Please enable cookies and try again.", status=400)
            else:
                request.session['oidc_attempted'] = True
                return redirect('%s?next=%s' % (self.OIDC_TRY_AUTH_URL, request.path))

        response = self.get_response(request)

        if self.OIDC_LOGOUT in request.path:
            request.session['oidc_attempted'] = True

        return response


class ForceAdminInEnglish:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            request.LANG = 'en'
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG

        return self.get_response(request)
