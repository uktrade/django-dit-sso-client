import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.utils import build_absolute_uri
from django.conf import settings

from ditsso.provider import DitSSOProvider


class DitSSOAdapter(OAuth2Adapter):
    provider_id = DitSSOProvider.id

    hostname = getattr(settings, 'DIT_SSO_HOSTNAME', 'dev.sso.uktrade.io')
    profile = getattr(settings, 'DIT_PROFILE_HOSTNAME', 'dev.profile.uktrade.io')
    access_token_url = 'https://{hostname}/oauth2/token/'.format(hostname=hostname)
    authorize_url = 'https://{hostname}/oauth2/authorize/'.format(hostname=hostname)
    supplier_url = 'https://{profile}/api/v1/directory/supplier/'.format(profile=profile)
    profile_url = 'https://{hostname}/oauth2/user-profile/v1/'.format(hostname=hostname)

    #TODO:  Temporary untill the callback url is fixed in SSO
    def get_previous_callback_url(self, request, app):
        return super().get_callback_url(request=request, app=app)

    def get_callback_url(self, request, app):
        callback_url = '/auth/callback'
        protocol = self.redirect_uri_protocol
        return build_absolute_uri(request, callback_url, protocol)
    # TODO: END

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'alt': 'json'})
        resp.raise_for_status()
        extra_data = resp.json()

        headers = {'Authorization': 'Bearer {}'.format(token.token)}
        resp = requests.get(self.supplier_url,
                            headers=headers)
        try:
            extra_data.update(resp.json)
        except TypeError:
            pass
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

oauth2_login = OAuth2LoginView.adapter_view(DitSSOAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DitSSOAdapter)