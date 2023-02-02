from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

# Create your views here.

# REST framework provides a set of already mixed-in generic views that we can use to trim down our views.py module even more.


#refactoring the views using generic class-based views
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# The core functionality is provided by the mixin classes, and we're simply adding the .ListCreateAPIView and .RetrieveUpdateDestroyAPIView classes to provide the actions that we want to support.