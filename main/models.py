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

class Comment(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField(default="")

    likers = models.ManyToManyField('auth.user', related_name="liked_comments", blank=True, null=True)
    dislikers = models.ManyToManyField('auth.user', related_name="disliked_comments", blank=True, null=True)

    video = models.ForeignKey('videos.Video', related_name='comments', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
