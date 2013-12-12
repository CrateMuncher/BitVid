import string
import django.contrib.auth.hashers
import django.core.exceptions
from django.db import models
from django.contrib.auth.models import BaseUserManager
import random
from django.contrib.auth.models import User as BaseUser
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from django.core.urlresolvers import reverse



class Video(models.Model):
    STATUS_UPLOADING = 'UP'
    STATUS_WAITING = 'WT'
    STATUS_TRANSCODING = 'TC'
    STATUS_ACTIVE = 'AC'
    STATUS_TAKENDOWN = 'TD'

    STATUS_CHOICES = (
        (STATUS_UPLOADING, 'Unconfirmed'),
        (STATUS_WAITING, 'Waiting for transcoder'),
        (STATUS_TRANSCODING, 'Transcoding'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_TAKENDOWN, 'Taken Down'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    title = models.CharField(max_length=64, default="")
    description = models.TextField(default="")

    uploader = models.ForeignKey('auth.user')

    likers = models.ManyToManyField('auth.user', related_name="liked_videoes", blank=True, null=True)
    dislikers = models.ManyToManyField('auth.user', related_name="disliked_videoes", blank=True, null=True)

    views = models.IntegerField(default=0)

    uploaded_date = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey('channels.Channel', related_name='video', blank=True, null=True)

			 
class Comment(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField(default="")

    likers = models.ManyToManyField('auth.user', related_name="liked_comments", blank=True, null=True)
    dislikers = models.ManyToManyField('auth.user', related_name="disliked_comments", blank=True, null=True)

    video = models.ForeignKey('Video', related_name='comments', blank=True, null=True)


class VideoFile(models.Model):
    format = models.CharField(max_length=5, default="")
    codec = models.CharField(max_length=128, default="")
    url = models.URLField(blank=True, null=True)

    video = models.ForeignKey('Video', related_name="video_files", blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
