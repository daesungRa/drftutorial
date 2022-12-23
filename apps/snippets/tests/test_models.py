"""
Test models in snippets app.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from apps.snippets.models import Snippet
from .mixins import CreateTestSnippetMixin


class SnippetTests(CreateTestSnippetMixin, TestCase):
    """
    Test module for Snippet model.
    """

    def setUp(self) -> None:
        self._create_test_snippet()

    def test_get_snippets(self) -> None:
        """Test snippet list"""
        snippets = Snippet.objects.all()
        self.assertEqual(len(snippets), 1)

    def test_get_snippets_by_owner(self) -> None:
        """Test snippet list by owner"""
        owner = User.objects.get(username=self.username)
        snippets = Snippet.objects.filter(owner=owner)
        self.assertEqual(len(snippets), 1)

    def test_create_and_get_snippet(self) -> None:
        """Test creation snippet"""
        title = 'My test snippet 02'
        code = 'print("hihi~")'
        owner = User.objects.get(username=self.username)
        self._create_test_snippet(title=title, code=code, owner=owner)

        try:
            snippet = Snippet.objects.filter(title__contains=title).first()
            snippets = Snippet.objects.filter(owner=owner)
        except Snippet.DoesNotExist:
            raise AssertionError('Snippet not created.')

        self.assertIn(code, snippet.code)
        self.assertEqual(len(snippets), 2)
