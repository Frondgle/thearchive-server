"""View module for handling requests about Arts"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from thearchiveapi.models import Art, Fan
from cloudinary.models import CloudinaryField
# from cloudinary import CloudinaryImage


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
        serializer = ArtSerializer(arts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def upload(file, **options):
    #     return cloudinary.uploader.upload(file, **options)



class ArtFanSerializer(serializers.ModelSerializer):
    """JSON serializer for Fan
    """
    class Meta:
        model = Fan
        fields = ('id', 'uid', 'username')


class ArtSerializer(serializers.ModelSerializer):
    """JSON serializer for Art
    """
    # fan = ArtFanSerializer(many=False)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Art
        fields = (
            'id',
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
            # 'fan',
            'tags'
        )

    def get_tags(self, obj):
        # Extract and serialize tag category names
        return [tag.category for tag in obj.tags.all()]
