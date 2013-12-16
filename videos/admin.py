from django.contrib import admin

# Register your models here.
from models import Video, VideoFile

admin.site.register(Video)

admin.site.register(VideoFile)
