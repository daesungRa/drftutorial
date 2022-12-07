"""
URLConf of snippet app.
"""

from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserList, UserDetail, SnippetList, SnippetDetail


app_name = 'snippets'
urlpatterns = [
    path('', SnippetList.as_view()),
    path('<int:pk>/', SnippetDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns=urlpatterns)
