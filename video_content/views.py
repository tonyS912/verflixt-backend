from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Video
from .serializers import VideoSerializer

#  TODO: Create test for it


class VideoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer

    queryset = Video.objects.all()
