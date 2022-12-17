"""
Mixins for quickstart app
"""

from django.contrib.auth.models import User


class UserTestMixin(object):
    """
    Mixin for user test.
    """

    username = 'tuser01'
    email = 'testuser01@test.py'
    password = 'ttt01'

    def _create_test_user(self, email: str = None, username: str = None, password: str = None) -> None:
        """Create User object"""
        target_username = username if username is not None else self.username
        target_email = email if email is not None else self.email
        target_password = password if password is not None else self.password

        # Check user existence.
        try:
            User.objects.get(username=target_username)
            return
        except User.DoesNotExist:
            pass

        # Create new user
        user = User(email=target_email, username=target_username)
        user.set_password(target_password)  # Set hashed password
        user.save()

    def setUp(self) -> None:
        """Setup default test user"""
        self._create_test_user()
