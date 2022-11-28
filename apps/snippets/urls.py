"""
URLConf of snippet app.
"""

from django.urls import path

from .views import snippet_list, snippet_detail


app_name = 'snippets'
urlpatterns = [
    path('', snippet_list),
    path('<int:pk>/', snippet_detail),
]
