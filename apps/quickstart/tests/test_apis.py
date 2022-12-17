"""
Test views in quickstart app.
"""

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from django.contrib.auth.models import User, Group

from apps.quickstart.serializers import UserSerializer, GroupSerializer

from .mixins import UserTestMixin


class BaseAPITestCase(UserTestMixin, APITestCase):
    """
    Base module for REST API test.
    """

    class Meta:
        abstract = True

    def setUp(self) -> None:
        """Setup default test user"""
        super(BaseAPITestCase, self).setUp()

        # Set authentication for REST API call
        test_user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=test_user)

        # Set request factory
        self.factory = APIRequestFactory()


class GetAndRetrieveTests(BaseAPITestCase):
    """
    Test get and retrieve api call.
    """

    def test_get_users(self) -> None:
        """Test user list"""
        url = '/quickstart/users/'
        response = self.client.get(url, format='json')

        # Response check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Serialized result check
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': self.factory.get(url)})
        self.assertEqual(response.json()['results'], serializer.data)

    def test_get_user(self) -> None:
        """Test single user"""
        user = User.objects.get(username=self.username)
        url = f'/quickstart/users/{user.id}/'
        response = self.client.get(url, format='json')

        # Response check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

        # Serialized result check
        serializer = UserSerializer(user, context={'request': self.factory.get(url)})
        self.assertEqual(response.data, serializer.data)

    def test_get_groups(self) -> None:
        """Test group list"""
        url = '/quickstart/groups/'
        response = self.client.get(url, format='json')

        # Response check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Serialized result check
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={'request': self.factory.get(url)})
        self.assertEqual(response.json()['results'], serializer.data)

    def test_get_group(self) -> None:
        pass


class CreateAndPutTests(BaseAPITestCase):
    """
    Test create and put api call.
    """

    def test_create_user(self) -> None:
        pass

    def test_put_user(self) -> None:
        pass


class DeleteTest(BaseAPITestCase):
    """
    Test delete api call.
    """

    def test_delete_user(self) -> None:
        pass
