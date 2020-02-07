from django.conf import settings


def oidc_op_logout(request):
    oidc_op_logout_endpoint = settings.OIDC_OP_LOGOUT_ENDPOINT
    redirect_url = request.build_absolute_uri(getattr(settings, 'LOGOUT_REDIRECT_URL', '/'))
    return '{}?redirect_uri={}'.format(oidc_op_logout_endpoint, redirect_url)
