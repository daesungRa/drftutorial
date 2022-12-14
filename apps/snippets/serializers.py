"""
Serializers of snippets app.
"""

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Snippet


# Use HyperlinkedModelSerializer instead of ModelSerializer.
# This used for dealing with relationships by hyperlinking.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    ```HyperlinkedModelSerializer``` has the following differences from ```ModelSerializer```.
        - It does not include the ```id``` field by default.
        - It includes a ```url``` field, using ```HyperlinkedIdentityField```.
        - Relationships use ```HyperlinkedRelatedField```, instead of ```PrimaryKeyRelatedField```.
    """
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets',)


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    """
    ```HyperlinkedModelSerializer``` has the following differences from ```ModelSerializer```.
        - It does not include the ```id``` field by default.
        - It includes a ```url``` field, using ```HyperlinkedIdentityField```.
        - Relationships use ```HyperlinkedRelatedField```, instead of ```PrimaryKeyRelatedField```.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    # Add a new 'highlight' field that is same type as the ```url``` field,
    # except that it points to the 'snippet-highlight' url pattern, instead of the 'snippet-detail' url pattern.
    # Because we've included format suffixed URLs such as '.json', we also need to indicate on the 'highlight' field
    # that any format suffixed hyperlinks it returns should use the '.html' suffix.
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style',)


# Use ModelSerializer by default


class DeprecatedUserSerializer(serializers.ModelSerializer):
    """
    DEPRECATED!

    User serializer. This is endpoints for User models.
        'Snippets' is a reverse relationship on the User model, it will not be included by default
        when using the ```ModelSerializer``` class, so we needed to add an explicit field for it.
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets',)


class DeprecatedSnippetSerializer(serializers.ModelSerializer):
    """
    DEPRECATED!

    Snippet serializer
        The create() and update() methods define how fully fledged instances
        are created or modified when calling serializer.save()
    """
    # 'Snippets' are associated with the user who created them(named by owner).
    # The 'source' argument controls which attribute is used to populate a field,
    # and can point at any attribute on the serialized instance.
    # It can also take the dotted notation shown below, in which case it will traverse the given attributes,
    # in a similar way as it is used with Django's template language.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        If this class is instance of ModelSerializer,
        Set the code below.
        """
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner',)

    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new 'Snippet' instance, given the validate data.
    #         :param validated_data: Validated data from .is_valid() method.
    #         :return: Created 'Snippet' instance.
    #     """
    #     return Snippet.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing 'Snippet' instance, given the validated data.
    #         :param instance: 'Snippet' instance to update.
    #         :param validated_data: Validated data from .is_valid() method.
    #         :return: Updated 'Snippet' instance.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
