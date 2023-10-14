import os.path
import subprocess

from .models import Video


def convert_video(source, resolution):
    source_name = os.path.splitext(source)[0]
    new_name = f'{source_name}_{resolution}.mp4'
    resolution_options = {
        '480p': 'hd480',
        '720p': 'hd720',
        '1080p': 'hd1080',
    }

    if resolution in resolution_options:
        cmd = f'ffmpeg -i "{source}" -s {resolution_options[resolution]} -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_name}"'
        conversion_start = subprocess.Popen(cmd, shell=True)
        conversion_start.wait()
        file_name = os.path.basename(source)
        video = Video.objects.get(video_file__icontains=file_name)
        new_relative_path = 'videos/{}'.format(os.path.basename(new_name))
        setattr(video, f'video_file_{resolution}', new_relative_path)
        video.save()
    else:
        print(f'invalid resolution {resolution}')