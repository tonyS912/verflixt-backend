from rest_framework import serializers
from .models import Video

#  TODO: Create test for it.

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
