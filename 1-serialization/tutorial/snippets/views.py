from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly

# Create your views here.


# The @api_view decorator can be used for writing function based views, and we can use the Response object to control the content and the status code of the response that's returned by the view.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users':
        reverse('user-list', request=request, format=format),
        'snippets':
        reverse('snippet-list', request=request, format=format)
    })


# REST framework provides a set of already mixed-in generic views that we can use to trim down our views.py module even more.


#refactoring the views using generic class-based views
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # We want to restrict the creation of snippets to authenticated users only, so we'll also add a permission class to the view.

    # We want to associate the created Snippet instance with the currently authenticated User instance,so we override
    # the perform_create() method on the view, and set the owner attribute of the saved snippet instance to the current user.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# The core functionality is provided by the mixin classes, and we're simply adding the .ListCreateAPIView and
# .RetrieveUpdateDestroyAPIView classes to provide the actions that we want to support.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer