"""
Add Snippet model to Django admin.
"""

from django.contrib.admin import register as admin_register
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

from .models import Snippet


@admin_register(Snippet)
class CustomSnippetAdmin(ModelAdmin):
    """
    Custom Snippet admin
    """

    fieldsets = (
        (
            'Update Snippet Values',
            {
                'fields': (
                    'title', 'code', 'linenos', 'language', 'style',
                )
            }
        ),
    )
    list_display = (
        'id', 'title', 'owner', 'view_highlighted', 'created',) + ModelAdmin.list_display
    ordering = ('-id',)
    list_filter = ModelAdmin.list_filter + ('title', 'owner',)
    search_fields = (
        'title__contains', 'code__contains', 'highlighted__contains', 'owner__username', 'language', 'style',)

    def view_highlighted(self, obj):
        url = f'/snippets/{obj.id}/highlight/'
        return format_html('<a href="{}">Snippet highlight</a>', url)

    view_highlighted.short_description = 'Highlighted'
