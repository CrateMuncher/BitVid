import string
import django.contrib.auth.hashers
from django.db import models
import random


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


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    nickname = models.CharField(max_length=64)

    login_token = models.CharField(max_length=64)

    channels = models.ManyToManyField('Channel')

    @staticmethod
    def signup(username, password, email):
        hashed_pass = django.contrib.auth.hashers.make_password(password)

    @staticmethod
    def authenticate_credentials(username, password):
        user = User.objects.get(username=username)

        if user is None:
            return None

        hashed_pass = django.contrib.auth.hashers.check_password(password, user.password, setter=user.set_password)

        if user.password == hashed_pass:
            new_token = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(64))
            user.login_token = new_token
            return user
        else:
            return None

    @staticmethod
    def authenticate_token(token):
        return User.objects.get(login_token=token)

    def set_password(self, new_password):
        self.password = django.contrib.auth.hashers.make_password(new_password)


class Comment(models.Model):
    author = models.OneToOneField('User')

    content = models.TextField()

    likers = models.ManyToManyField('User', related_name="liked_comments")
    dislikers = models.ManyToManyField('User', related_name="disliked_comments")