from django.db import models
from datetime import date


class Video(models.Model):
    created_at = models.DateField(default=date.today)  # date from today how implement the Video
    created_from = models.CharField(max_length=100, default="Guest", blank=True)  # creator of the video content, defaul is Guest but can be empty
    title = models.CharField(max_length=180)  # Video title/name == required, weil blank=True an der stelle fehlen würde
    description = models.TextField()  # description about the Videostory == required, weil black=True an der fehlen würde
    video_file = models.FileField(upload_to='videos', blank=False, null=False)  # Uploadfield for the Video, it can be empty and null. that makes them optional
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True)  #  the same video above but different quality

    def __str__(self) -> str:
        return self.title  # returns the title for the backend view
