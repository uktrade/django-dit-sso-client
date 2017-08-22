import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.utils import build_absolute_uri
from django.conf import settings

from ditsso_internal.provider import DitSSOInternalProvider


class DitSSOInternalAdapter(OAuth2Adapter):
    provider_id = DitSSOInternalProvider.id
    hostname = settings['DIT_SSO_INTERNAL_HOSTNAME'] or 'staff-sso-staging.herokuapp.com'
    access_token_url = 'https://{hostname}/o/token/'.format(hostname=hostname)
    authorize_url = 'https://{hostname}/o/authorize/'.format(hostname=hostname)
    profile_url = 'https://{hostname}/o/user-profile/v1/'.format(hostname=hostname)

    def get_callback_url(self, request, app):
        callback_url = '/auth/callback'
        protocol = self.redirect_uri_protocol
        return build_absolute_uri(request, callback_url, protocol)

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'alt': 'json'})
        resp.raise_for_status()
        extra_data = resp.json()

        try:
            extra_data.update(resp.json)
        except TypeError:
            pass
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

oauth2_login = OAuth2LoginView.adapter_view(DitSSOInternalAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DitSSOInternalAdapter)