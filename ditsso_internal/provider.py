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
        uid = response['email']
        return uid

    def extract_email_addresses(self, response):
        email = response.get('email', None)
        return [EmailAddress(email=email, verified=True)]

    def extract_extra_data(self, data):
        return data

    def extract_common_fields(self, data):
        common_data = {}
        first_name = data.get('first_name')
        if first_name:
            common_data['first_name'] = first_name
        last_name = data.get('last_name')
        if last_name:
            common_data['last_name'] = last_name

        email = data.get('email')
        if email:
            common_data['email'] = email

        username = data.get('username', '.'.join([x for x in [first_name, last_name] if x]))
        if not username and email:
            username = email.split('@').pop(0)

        if username:
            common_data['username'] = username

        return common_data

provider_classes = [DitSSOInternalProvider]
