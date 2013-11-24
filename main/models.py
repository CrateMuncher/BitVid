import django.contrib.auth.models
from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=64)

    is_active = models.BooleanField()

    videoes = models.ForeignKey('Video')

class Video(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()

    is_active = models.BooleanField()

    uploader = models.OneToOneField('User')

    likers = models.ManyToManyField('User', related_name="liked_videoes")
    dislikers = models.ManyToManyField('User', related_name="disliked_videoes")

    views = models.IntegerField()

    comments = models.ForeignKey('Comment')

class User(django.contrib.auth.models.AbstractUser):
    nickname = models.CharField(max_length=64)

    channels = models.ManyToManyField('Channel')

class Comment(models.Model):
    author = models.OneToOneField('User')

    content = models.TextField()

    likers = models.ManyToManyField('User', related_name="liked_comments")
    dislikers = models.ManyToManyField('User', related_name="disliked_comments")