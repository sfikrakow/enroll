from mozilla_django_oidc.views import OIDCAuthenticationRequestView


class OIDCAuthenticationNoPromptRequestView(OIDCAuthenticationRequestView):
    def get_extra_params(self, request):
        params = super().get_extra_params(request)
        params["prompt"] = "none"
        return params
