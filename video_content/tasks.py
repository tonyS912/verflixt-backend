import subprocess
import os

from django.conf import settings
from django.db import transaction

from .models import Video


@transaction.atomic
def convert_480p(video_pk):
    video = Video.objects.get(pk=video_pk)
    source = video.video_file.path
    target = source + "_480p.mp4"
    cmd = (
        'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23c:a aac -strict -2 "{}"'.format(source, target)
    )
    subprocess.run(cmd, shell=True)
    relative_target = os.path.relpath(target, settings.MEDIA_ROOT)
    video.video_file_480p.name = relative_target
    video.save()
