import string
import django.contrib.auth.hashers
import django.core.exceptions
from django.db import models
from django.contrib.auth.models import BaseUserManager
import random
from django.contrib.auth.models import AbstractBaseUser
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

    uploader = models.ForeignKey('User')

    likers = models.ManyToManyField('User', related_name="liked_videoes", blank=True, null=True)
    dislikers = models.ManyToManyField('User', related_name="disliked_videoes", blank=True, null=True)

    views = models.IntegerField(default=0)

    uploaded_date = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey('channels.Channel', related_name='video', blank=True, null=True)

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()

	if not username:
	    raise ValueError("The username cannot be blank")
        email = self.normalize_email(email)

	user = self.model(username=email,last_login=now, registration_date=now,
	                  **extra_fields)
        user.set_password(password)
	user.save()

	return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
	                         **extra_fields)

    def create_superuser(self,username,email,password=None, **extra_fields):
        return self._create_user(username,email,password,False,False, 
	                         **extra_fields)

class User(AbstractBaseUser):
    STATUS_UNCONFIRMED = 'UC'
    STATUS_ACTIVE = 'AC'
    STATUS_DISABLED = 'DS'

    STATUS_CHOICES = (
        (STATUS_UNCONFIRMED, 'Unconfirmed'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DISABLED, 'Disabled')
    )


    username = models.CharField(max_length=64, unique=True, default="")
    email = models.EmailField(max_length=256, default="")
    nickname = models.CharField(max_length=64, default="")

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    login_token = models.CharField(max_length=64, default="")

    tags = models.ManyToManyField('Tag', related_name="videoes", blank=True, null=True)

    channels = models.ManyToManyField('channels.Channel', related_name="members", blank=True, null=True)

    registration_date = models.DateTimeField(auto_now_add=True)

    #Used by Django's built-in auth system
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()


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
