from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import DitSSOProvider

urlpatterns = default_urlpatterns(DitSSOProvider)