from django.contrib import admin

# Register your models here.


from models import Video, Comment, VideoFile, Tag

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(VideoFile)
admin.site.register(Tag)