"""
URLConf of snippet app.
"""

from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import api_root, SnippetHighlight, UserList, UserDetail, SnippetList, SnippetDetail


urlpatterns = format_suffix_patterns(urlpatterns=[
    path(r'', api_root),
    path(r'snippets/', SnippetList.as_view(), name='snippet-list'),
    path(r'snippets/<int:pk>/', SnippetDetail.as_view(), name='snippet-detail'),
    path(r'snippets/<int:pk>/highlight/',
         SnippetHighlight.as_view(),
         name='snippet-highlight'),  # Using HTML renderer from REST framework
    path(r'users/', UserList.as_view(), name='snippet-user-list'),
    path(r'users/<int:pk>/', UserDetail.as_view(), name='snippet-user-detail'),
])
