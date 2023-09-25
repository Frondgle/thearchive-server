"""View module for handling requests about Arts"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from thearchiveapi.models import Art, Fan

class ArtView(ViewSet):
    """the sonatore archive Art ViewSets"""

    def retrieve(self, request, pk):
        """Handle GET/retrieve requests for a single art

        Returns:
            Response -- JSON serialized art
        """
        try:
            art = Art.objects.get(pk=pk)
            serializer = ArtSerializer(art)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Art.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET/List requests to get All Arts
        and filter Arts by tag
        Returns:
            Response -- JSON serialized list of arts
        """
        arts = Art.objects.all()

        tag = request.query_params.get('tag', None)
        print('tag', tag)
        if tag is not None:
            arts = arts.filter(tag=tag)

        serializer = ArtSerializer(arts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArtFanSerializer(serializers.ModelSerializer):
    """JSON serializer for Fan
    """
    class Meta:
        model = Fan
        fields = ('id', 'uid', 'username')

class ArtSerializer(serializers.ModelSerializer):
    """JSON serializer for Art
    """
    fan = ArtFanSerializer(many=False)
    class Meta:
        model = Art
        fields = (
            'pic', 
            'title', 
            'code', 
            'style', 
            'location', 
            'description', 
            'color', 
            'frame_type', 
            'mods', 
            'date_created', 
            'film_type', 
            'malfunction', 
            'fan', 
            'tag'
            )
