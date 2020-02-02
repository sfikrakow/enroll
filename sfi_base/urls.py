from django.conf.urls import url
from django.urls import include

from .views import OIDCLogoutView, OIDCAuthenticationNoPromptRequestView

urlpatterns = [
    url(r'^logout/$', OIDCLogoutView.as_view(), name='oidc_logout'),
    url(r'^tryauthenticate/', OIDCAuthenticationNoPromptRequestView.as_view(), name='oidc_try_authenticate'),
    url(r'^', include('mozilla_django_oidc.urls')),
]
