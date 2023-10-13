from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Video


class VideoModelTest(TestCase):
    def test_video_creation(self):
        # Erstellen Sie ein Beispiel-Video
        video = Video.objects.create(
            title="Test Video",
            description="This is a test video",
            video_file=SimpleUploadedFile("file.mp4", b"file_content")
        )

        # Überprüfen Sie, ob das Video erfolgreich erstellt wurde
        self.assertIsInstance(video, Video)
        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.description, "This is a test video")

        #  Ausgabe für bessere Nachvollziehbarkeit
        print('Testcase "test_video_creation" erfolgreich abgeschlossen.')


class VideoViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
