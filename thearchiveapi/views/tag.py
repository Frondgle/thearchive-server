"""View module for handling requests about Tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from thearchiveapi.models import Tag


class TagView(ViewSet):
    """the sonatore archive Tag view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get All Tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    """
    class Meta:
        model = Tag
        fields = (
            'id', 
            'category'
            )
