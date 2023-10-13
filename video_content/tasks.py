import os.path
import subprocess

from .models import Video


def convert_480p(source):
    print(source)
    source_name = os.path.splitext(source)[0]
    print(source_name)
    new_name = source_name + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_name)
    conversion_start = subprocess.Popen(cmd, shell=True)
    conversion_start.wait()
    file_name = os.path.basename(source)
    video = Video.objects.get(video_file__icontains=file_name)
    new_relative_path = 'videos/{}'.format(os.path.basename(new_name))
    video.video_file_480p = new_relative_path
    video.save()
