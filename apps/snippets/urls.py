"""
URLConf of snippet app.
"""

from django.urls import path, include

from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.routers import DefaultRouter

from ..quickstart.views import UserViewSet as QuickstartUserViewSet
from .views import UserViewSet, SnippetViewSet, api_root


# Tutorial6: Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'user-snippets', UserViewSet, basename='user-snippet')
router.register(r'users', QuickstartUserViewSet, basename='users')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]


# DEPRECATED!!
# Notice: "Expected type 'ViewSetMixin'" warning is caused by specific version of DRF or PyCharm editor.
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list',
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})
Deprecated_urlpatterns = format_suffix_patterns(urlpatterns=[
    path(r'', api_root),
    path(r'snippets/', snippet_list, name='snippet-list'),
    path(r'snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path(r'snippets/<int:pk>/highlight/',
         snippet_highlight,
         name='snippet-highlight'),  # Using HTML renderer from REST framework
    path(r'users/', user_list, name='snippet-user-list'),
    path(r'users/<int:pk>/', user_detail, name='snippet-user-detail'),
])
