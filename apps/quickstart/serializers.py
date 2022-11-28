"""
Serializers of quickstart app.
"""

from django.contrib.auth.models import User, Group

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User Serializer of quickstart app"""

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Group Serializer of quickstart app"""

    class Meta:
        model = Group
        fields = ('url', 'name',)
