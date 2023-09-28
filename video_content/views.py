from rest_framework import viewsets

from .models import Video
from .serializers import VideoSerializer


# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
