from mozilla_django_oidc import views
from mozilla_django_oidc.views import OIDCAuthenticationRequestView


class OIDCLogoutView(views.OIDCLogoutView):
    def get(self, request):
        """
        The OIDCLogoutView only implements logout via a post request, but we want a get request.
        Therefore allow that here
        """
        return self.post(request)


class OIDCAuthenticationNoPromptRequestView(OIDCAuthenticationRequestView):
    def get_extra_params(self, request):
        params = super().get_extra_params(request)
        params["prompt"] = "none"
        return params
