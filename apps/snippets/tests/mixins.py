"""
Mixins for snippets app.
"""

from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from apps.quickstart.tests.mixins import CreateTestUserMixin
from apps.snippets.models import Snippet


class CreateTestSnippetMixin(CreateTestUserMixin):
    """
    Mixin for snippet testing.
    """

    title = 'My test snippet 01'
    code = 'print("Hi, this is test code 01!!")'

    def _create_test_snippet(self,
                             title: str = None,
                             code: str = None,
                             linenos: bool = None,
                             language: str = None,
                             style: str = None,
                             owner: User = None):
        # Set target variable
        target_title = title if title is not None else self.title
        target_code = code if code is not None else self.code
        target_linenos = linenos if linenos is not None else False
        target_language = language if language is not None else 'python'
        target_style = style if style is not None else 'fruity'

        # Create test user if it doesn't exist and set it to owner field.
        self._create_test_user()
        target_owner = owner if owner is not None else User.objects.get(username=self.username)

        # Create new snippet
        snippet = Snippet(
            title=target_title,
            code=target_code,
            linenos=target_linenos,
            language=target_language,
            style=target_style,
            owner=target_owner,
        )
        # This action involves using 'pygments' package to make a 'highlighted' field
        # that are HTML representation of the code snippet.
        snippet.save()


class APITestRequiredMixin(CreateTestUserMixin):
    """
    Mixin for API testing.
    """

    def _set_required_config_to_api_call(self) -> None:
        # Create test user if it doesn't exist.
        self._create_test_user()

        # Set authentication for REST API call
        test_user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=test_user)

        # Set request factory
        self.factory = APIRequestFactory()
