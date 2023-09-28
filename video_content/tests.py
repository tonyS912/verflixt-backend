from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Video


# Create your tests here.
class VideoModelTest(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video.",
            video_file=SimpleUploadedFile("file.mp4", b"file_content"),
        )

    def test_str(self):
        self.assertEqual(str(self.video), "Test Video")


class VideoSerializerTest(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video.",
            video_file=SimpleUploadedFile("file.mp4", b"file_content"),
        )