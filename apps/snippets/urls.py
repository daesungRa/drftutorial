"""
URLConf of snippet app.
"""

from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import SnippetList, SnippetDetail


app_name = 'snippets'
urlpatterns = [
    path('', SnippetList.as_view()),
    path('<int:pk>/', SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns=urlpatterns)
