OIDC_OP_LOGOUT_URL_METHOD = 'sfi_base.utils.oidc_op_logout'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_RP_SCOPES = 'openid email'

LOGIN_URL = 'oidc_authentication_init'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/certs'
OIDC_OP_LOGOUT_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/logout'

OIDC_ADMIN_ROLE = 'admins'
