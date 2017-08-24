from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class Scope(object):
    READ = 'read'
    WRITE = 'write'

class DitSSOInternalAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('link')


class DitSSOInternalProvider(OAuth2Provider):
    id = 'ditsso-internal'
    name = 'DitSSO-Internal'
    account_class = DitSSOInternalAccount

    def get_default_scope(self):
        return [Scope.READ]

    def extract_uid(self, response):
        uid = response['id']
        return uid

    def extract_email_addresses(self, response):
        email = response.get('email', None)
        return [EmailAddress(email=email, verified=True)]


provider_classes = [DitSSOInternalProvider]
