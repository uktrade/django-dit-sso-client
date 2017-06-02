==============
DIT sso client
==============

Simple extension to django-allauth to create provider classes for DIT sso using Oauth2


Quickstart
----------

1. Add to installed apps dit-sso-client and allauth app
    INSTALLED_APPS = [
        ...
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'dit-sso-client',
    ]

2. Include the URLconf in your project urls.py like this::

    url(r'^accounts/', include('allauth.urls')),


4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a Social app with key and secret

5. Set up callback url on the sso provider
{HOSTNAME}/accounts/social/ditsso/callback/


