from django.db import models
from datetime import date


# Create your models here.
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    created_from = models.CharField(max_length=100, default="Guest", blank=True)
    title = models.CharField(max_length=180)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True)

    def __str__(self) -> str:
        return self.title
