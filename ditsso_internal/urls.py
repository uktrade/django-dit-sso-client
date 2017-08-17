from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import DitSSOInternalProvider

urlpatterns = default_urlpatterns(DitSSOInternalProvider)