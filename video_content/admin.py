from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class VideoAdmin(ImportExportModelAdmin):
    list_display = (
        "title",
        "created_at",
        "created_from",
        "description",
    )  # Fields will be shown in list-view

    fields = (
        "title",
        "created_at",
        "created_from",
        "description",
        "video_file",
    )  # Field can be edited


admin.site.register(Video, VideoAdmin)


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
