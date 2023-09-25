"""View module for handling requests about Tags"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from thearchiveapi.models import Tag

class TagView(ViewSet):
    """the sonatore archive Tag view"""

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized tag instance
        """

        new_tag = Tag.objects.create(
            category=request.data["category"]
        )
        serializer = TagSerializer(new_tag)
        return Response(serializer.data)

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

    def update(self, request, pk=None):
        """Handle PUT requests for a tag - replaces entire object
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.category = request.data["category"]
            tag.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response("Oops 404! Tag not found", status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response(
                {'Oops, 404! Tag not found': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {'Oops, 500! My bad': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    """
    class Meta:
        model = Tag
        fields = (
            'id', 
            'category'
            )
