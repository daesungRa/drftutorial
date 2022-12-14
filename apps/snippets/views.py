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

    rest_framework.viewsets:
        ```ViewSet``` classes are almost the same thing as ```View``` classes,
        except that they provide operations such as ```retrieve```, or ```update```,
        and not method handlers such as ```get``` or ```put```.

[!!] If you look at the DEPRECATED views from the bottom of this page,
You'll see how much code has been simplified as you go through the tutorial.
"""

from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from rest_framework import viewsets

from .models import Snippet
from .serializers import UserSerializer, SnippetSerializer
from .permissions import IsOwnerOrReadOnly


# Tutorial6: 'UserViewSet' that is combination of 'UserList' and 'UserDetail' view classes.
# Tutorial6: 'SnippetViewSet' that is combination of 'SnippetList', 'SnippetDetail' and 'SnippetHighlight' view classes.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions.
        ```ReadOnlyModelViewSet``` class provide the default 'read-only' operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
        ```ModelViewSet``` class is used to get the complete set of default read and write operations.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        """
        This method decorated with ```action``` decorator to create a custom action.

        ```action``` decorator creates custom endpoints
        that don't fit into the standard 'create'/'update'/'delete' style.

        And custom actions which use the ```@action``` decorator will respond to 'GET' requests by default.
        We can use the 'methods' argument if we wanted an action that responded to 'POST' requests.

        The URLs for custom actions by default depend on the method name itself.
        If you want to change the way url should be constructed,
        you can include ```url_path``` as a decorator keyword argument.
        """
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        """
        Same as 'perform_create' method of the SnippetList view.
        """
        serializer.save(owner=self.request.user)


# Tutorial5: Single entry point for the snippet's root API
# Tutorial5: Code highlighting endpoints using pre-rendered HTML plugin provided by REST framework.


@api_view(['GET'])
def api_root(request, format=None):
    """
    DEPRECATED!

    Single entry point to provide 'snippets' and 'users'.
        :return:
            Using REST framework's ```reverse``` function in order to return fully-qualified URLs.
            and a URL patterns like specified below will also be declared in the ```snippets/urls.py``` module.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippet-users': reverse('snippet-user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })


class SnippetHighlight(generics.GenericAPIView):
    """
    DEPRECATED!

    Code highlighting endpoint.
        Instead of using a concrete generic view, we'll use the base class for representing instances,
        and create our own ```.get()``` method.
        We're not returning an object instance, but instead a property of an object instance.
    """
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# CBV for user model


class UserList(generics.ListAPIView):
    """
    DEPRECATED!

    User list view.
    This is used for read-only views for user representation only.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    DEPRECATED!

    User detail view.
    This is used for read-only views for user representation only.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Class based views using generic class-based views.


class SnippetList(generics.ListCreateAPIView):
    """
    DEPRECATED!

    DRF provides a set of already mixed-in generic views like ```ListCreateAPIView```
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Overridden method from ```rest_framework.mixins.CreateModelMixin```:
            This method allows us to modify how the instance save is managed,
            and handle any information that is implicit in the incoming request or reqeusted URL.
        """

        # The ```CreateModelMixin.create()``` method of this serializer will now be passed an additional 'owner' field,
        # along with the validated data from the request.
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    DEPRECATED!

    DRF provides a set of already mixed-in generic views like ```RetrieveUpdateDestroyAPIView```
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# Class based views using mixing classes.


class DeprecatedMixinSnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    DEPRECATED!

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
    DEPRECATED!

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
