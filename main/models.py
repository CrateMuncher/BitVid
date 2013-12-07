import string
import django.contrib.auth.hashers
import django.core.exceptions
from django.db import models
import random
from django.core.exceptions import ValidationError
import re

class Channel(models.Model):
    name = models.CharField(max_length=64, unique=True)

    STATUS_ACTIVE = 'AC'
    STATUS_DELETED = 'DL'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DELETED, 'Deleted'),
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    subscribers = models.ManyToManyField('User', related_name="subscriptions")

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError('Name is to short (<2 Chars)')

        if not re.match(r'^[A-Za-z0-9_-]+$', self.name):
            raise ValidationError("Name must only contain letters, numbers, underscores and hyphens.")

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

    uploader = models.ForeignKey('User')

    likers = models.ManyToManyField('User', related_name="liked_videoes", blank=True, null=True)
    dislikers = models.ManyToManyField('User', related_name="disliked_videoes", blank=True, null=True)

    views = models.IntegerField(default=0)

    uploaded_date = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey('Channel', related_name='video', blank=True, null=True)


class User(models.Model):
    STATUS_UNCONFIRMED = 'UC'
    STATUS_ACTIVE = 'AC'
    STATUS_DISABLED = 'DS'

    STATUS_CHOICES = (
        (STATUS_UNCONFIRMED, 'Unconfirmed'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DISABLED, 'Disabled')
    )
    username = models.CharField(max_length=64, unique=True, default="")
    password = models.CharField(max_length=256, default="")
    email = models.EmailField(max_length=256, default="")
    nickname = models.CharField(max_length=64, default="")

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    login_token = models.CharField(max_length=64, default="")

    tags = models.ManyToManyField('Tag', related_name="videoes", blank=True, null=True)

    channels = models.ManyToManyField('Channel', related_name="members", blank=True, null=True)

    registration_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def signup(username, password, email):
        hashed_pass = django.contrib.auth.hashers.make_password(password)

        if User.objects.filter(username=username).exists():
            return None

        user = User.objects.create(username=username, password=hashed_pass, email=email, nickname=username)
        user.save()

        return user

    @staticmethod
    def authenticate_credentials(username, password):

        if not User.objects.filter(username=username).exists():
            return None

        user = User.objects.get(username=username)

        valid_password = django.contrib.auth.hashers.check_password(password, user.password, setter=user.set_password)

        if valid_password:
            user.refresh_token()
            user.save()
            return user
        else:
            return None

    @staticmethod
    def authenticate_token(token):
        if User.objects.filter(login_token=token).exists():
            return User.objects.get(login_token=token)
        else:
            return None

    def set_password(self, new_password):
        self.password = django.contrib.auth.hashers.make_password(new_password)
        self.save()

    def refresh_token(self):
        new_token = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(64))
        self.login_token = new_token
        self.save()
        return new_token


class Comment(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField(default="")

    likers = models.ManyToManyField('User', related_name="liked_comments", blank=True, null=True)
    dislikers = models.ManyToManyField('User', related_name="disliked_comments", blank=True, null=True)

    video = models.ForeignKey('Video', related_name='comments', blank=True, null=True)


class VideoFile(models.Model):
    format = models.CharField(max_length=5, default="")
    codec = models.CharField(max_length=128, default="")
    url = models.URLField(blank=True, null=True)

    video = models.ForeignKey('Video', related_name="video_files", blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
