from django.shortcuts import render
import boto.s3.connection
import boto.s3.key
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import re

from models import VideoFile, Video
from channels.models import Channel

import bitvid.dbinfo
try:
    from bitvid.settings import VIDEO_BUCKET_NAME
except:
    VIDEO_BUCKET_NAME = "bitvid-video"

# Create your views here.
@login_required
def upload(request):
    if request.method == "GET":

    	chans = Channel.objects.filter(members__in=[request.user])
        return render(request, "upload.html",{"channels":chans})
    else:

        user = request.user
        file = request.FILES.get("file", None)

        if file is None:
            return HttpResponseBadRequest("You did not pass a file.")

        title = request.POST.get("title", "")
        desc = request.POST.get("desc", "")
        channel_id_str = request.POST.get("channel", "1")

        try:
            channel_id = int(channel_id_str)
        except ValueError:
            return HttpResponseBadRequest("Channel ID must be an integer")

        if title == "":
            return HttpResponseBadRequest("Title must not be empty.")

        if not re.match(r'^.{0,2000}$', title):
            return HttpResponseBadRequest("Description must not be longer than 2000 characters.")

        if not Channel.objects.filter(pk=channel_id).exists():
            return HttpResponseBadRequest("Channel ID must be a valid channel.")

        channel = Channel.objects.get(pk=channel_id)

        if not channel.members.filter(id=user.id).exists():
            return HttpResponseBadRequest("You do not own that channel.")


        video = Video.objects.create(uploader=user)
        video.title = title
        video.desciption = desc
        video.channel = channel
        video.save()

        video_file = VideoFile.objects.create()
        video_file.save()
        video_file.format = file.content_type

        video.video_files.add(video_file)

        video_file.save()
        video.save()

        conn = boto.s3.connection.S3Connection(bitvid.dbinfo.AWS_ACCESS, bitvid.dbinfo.AWS_SECRET)

        bucket = conn.get_bucket(VIDEO_BUCKET_NAME)
        bucket.set_acl("public-read")
        key = boto.s3.key.Key(bucket)

        video_path = str(video.id) + "/" + "original.mp4"

        video_file.url = "http://"+VIDEO_BUCKET_NAME +".s3.amazonaws.com/"+video_path #"http://d6iy9bzn1qbz8.cloudfront.net/" + video_path

        key.key = video_path
        key.set_contents_from_filename(file.temporary_file_path())

        key.set_acl('public-read')

        conn.close()

        video_file.save()
        return HttpResponse(str(video.id))

def view_video(request, video_id):
    if not Video.objects.filter(pk=video_id).exists():
        render(request, "notfound.html", {"error": "Video not found."})

    video = Video.objects.get(pk=video_id)
    return render(request, "view_video.html", {"video": video})