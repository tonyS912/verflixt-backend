from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Video
from .serializers import VideoSerializer

#  TODO: Create test for it


#  @permission_classes(IsAuthenticated)
class VideoViewSet(viewsets.ModelViewSet):
    #  authentication_classes = [TokenAuthentication]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
