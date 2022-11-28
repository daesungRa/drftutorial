"""
Serializers of snippets app.
"""

from rest_framework import serializers

from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    """
    Snippet serializer
        The create() and update() methods define how fully fledged instances
        are created or modified when calling serializer.save()
    """

    class Meta:
        """
        If this class is instance of ModelSerializer,
        Set the code below.
        """
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style',)

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
