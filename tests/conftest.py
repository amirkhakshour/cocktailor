import os
import json

import django
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import AnonymousUser
from django.test.client import Client

from rest_framework.authtoken.models import Token


def pytest_configure(config):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()


def pytest_unconfigure(config):
    # do cleanup
    pass


class ApiClient(Client):
    """GraphQL API client."""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", AnonymousUser())
        self._user = None
        self.token = None
        self.user = user
        self.app_token = None
        if not user.is_anonymous:
            self.token = self._get_user_token(user)

        super().__init__(*args, **kwargs)

    def _get_user_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def _base_environ(self, **request):
        environ = super()._base_environ(**request)
        if not self.user.is_anonymous:
            environ["HTTP_AUTHORIZATION"] = f"Token {self.token}"
        return environ

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        if not user.is_anonymous:
            self.token = self._get_user_token(user)

    def api_call(self, url_name, method, url_kwargs=None, data=None):
        # @todo add multipart post capability
        if url_kwargs is None:
            url_kwargs = {}

        if "version" not in url_kwargs:
            url_kwargs.update({"version": 1})
        try:
            url = reverse(url_name, kwargs=url_kwargs)
        except NoReverseMatch:
            url = url_name
        method = getattr(super(), method.lower())
        kwargs = {"content_type": "application/json"}

        if data:
            response = method(url, json.dumps(data), **kwargs)
        else:
            response = method(url, **kwargs)

        return response
