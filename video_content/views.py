from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from .models import Video
from .serializers import VideoSerializer

#  TODO: Create test for it


@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer

    queryset = Video.objects.all()
