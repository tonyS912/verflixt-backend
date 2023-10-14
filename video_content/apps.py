from django.apps import AppConfig


class VideoContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_content'

    def ready(self):
        from . import signals
