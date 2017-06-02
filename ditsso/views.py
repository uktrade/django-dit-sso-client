import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.utils import build_absolute_uri

from ditsso.provider import DitSSOProvider


class DitSSOAdapter(OAuth2Adapter):
    provider_id = DitSSOProvider.id
    access_token_url = 'https://dev.sso.uktrade.io/oauth2/token/'
    authorize_url = 'https://dev.sso.uktrade.io/oauth2/authorize/'
    suplier_url = 'https://dev.profile.uktrade.io/api/v1/directory/supplier/'
    profile_url = 'https://dev.sso.uktrade.io/oauth2/user-profile/v1/'

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

        headers = {'Authorization': 'Bearer {}'.format(token.token)}
        resp = requests.get(self.suplier_url,
                            headers=headers)
        try:
            extra_data.update(resp.json)
        except Exception as e:
            pass
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

oauth2_login = OAuth2LoginView.adapter_view(DitSSOAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DitSSOAdapter)