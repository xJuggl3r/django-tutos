# The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the snippet
# instances into representations such as json. We can do this by declaring serializers that work very similar to Django's forms.

from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']