import os
import django_rq

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Video
from .tasks import convert_video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video was saved')
    if created:
        print('New video was created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.video_file.path, "480p")
        queue.enqueue(convert_video, instance.video_file.path, "720p")
        queue.enqueue(convert_video, instance.video_file.path, "1080p")


# Help function to delete files
def _delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        _delete_file(instance.video_file.path)
    if instance.video_file_480p:
        _delete_file(instance.video_file_480p.path)
    if instance.video_file_720p:
        _delete_file(instance.video_file_720p.path)
    if instance.video_file_1080p:
        _delete_file(instance.video_file_1080p.path)
