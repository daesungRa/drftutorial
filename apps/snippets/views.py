"""
Views of snippets app.
    rest_framework.request.Request:
        The core functionality of the ```Request``` object is the ```request.data``` attribute,
        which is similar to ```request.POST```, but more useful for working with Web APIs.
    rest_framework.response.Response:
        This is a type of ```TemplateResponse``` that takes unrendered content
        and uses content negotiation to determine the correct content type to return to the client.
    rest_framework.status:
        REST framework provides more explicit identifiers for each status code,
        such as ```HTTP_400_BAD_REQUEST``` in this module.
        It's a good idea to use these throughout rather than using numeric identifiers.
    rest_framework.decorators.api_view:
        This wrapper provides a few bits of functionality such as making sure
        you receive ```Request``` instances in your view,
        and adding context to ```Response``` objects so that content negotiation can be performed.
    rest_framework.views.APIView:
        This module is used for class-based views, a powerful pattern
        that allows us to reuse common functionality, and helps us keep our code DRY.
"""

from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import mixins
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer


# Class based views using generic class-based views.


class SnippetList(generics.ListCreateAPIView):
    """
    DRF provides a set of already mixed-in generic views like ```ListCreateAPIView```
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    DRF provides a set of already mixed-in generic views like ```RetrieveUpdateDestroyAPIView```
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# Class based views using mixing classes.


class DeprecatedMixinSnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    The base class, ```GenericAPIView``` provides the core functionality,
    and the mixin classes provide the ```.list()``` and ```.create()``` actions.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)


class DeprecatedMixinSnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Again we're using the ```GenericAPIView``` class to provide the core functionality,
    and adding in mixins to provide the ```.retrieve()```, ```.update()``` and ```.destroy()``` actions.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request=request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request=request, *args, **kwargs)


# Class based views using APIView.


class DeprecatedSnippetList(APIView):
    """
    DEPRECATED!

    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeprecatedSnippetDetail(APIView):
    """
    DEPRECATED!

    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Function based views.


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    DEPRECATED!

    List all code snippets, or create a new snippet.
        :param request: Http request object.
        :return: Jsonify object formed by request method.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)

        return Response(serializer.data)
        # return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        """
        rest_framework.request.Request:
            This object has ```request.data``` attribute
            that is commonly used in 'POST', 'PUT', and 'DELETE' methods.
        """
        serializer = SnippetSerializer(data=request.data)
        # data = JSONParser().parse(request)
        # serializer = SnippetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    DEPRECATED!

    Retrieve, update or delete a code snippet.
        :param request: Http request object.
        :param pk: Target object's primary key.
        :return: Detailed data of specific snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        # return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)

        return Response(serializer.data)
        # return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        """
        rest_framework.request.Request:
            This object has ```request.data``` attribute
            that is commonly used in 'POST', 'PUT', and 'DELETE' methods.
        """
        serializer = SnippetSerializer(snippet, data=request.data)
        # data = JSONParser().parse(request)
        # serializer = SnippetSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return JsonResponse(serializer.data)
        # return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        # return HttpResponse(status=204)
