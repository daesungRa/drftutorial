"""
Test models in quickstart app.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from .mixins import CreateTestUserMixin


class UserTests(CreateTestUserMixin, TestCase):
    """
    Test module for Django User model.
    """

    def setUp(self) -> None:
        """Setup default test user"""
        self._create_test_user()

        super(UserTests, self).setUp()

    def test_get_user(self) -> None:
        """User model test"""
        user = User.objects.get(username=self.username)

        # Default info check
        self.assertEqual(user.email, self.email)

        # User password check
        self.assertEqual(user.check_password(self.password), True)
        self.assertEqual(user.check_password('ttt02'), False)

    def test_create_user(self) -> None:
        """User creation test"""
        email = 't2@test.py'
        username = 'tuser02'
        password = 'ttt02'
        self._create_test_user(email=email, username=username, password=password)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)
        self.assertEqual(user.check_password('ttt03'), False)
