from django.conf.urls import url
from django.urls import include

from .views import OIDCAuthenticationNoPromptRequestView

urlpatterns = [
    url(r'^tryauthenticate/', OIDCAuthenticationNoPromptRequestView.as_view(), name='oidc_try_authenticate'),
    url(r'^', include('mozilla_django_oidc.urls')),
]
