import string
import django.contrib.auth.hashers
import django.core.exceptions
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
    STATUS_UNCONFIRMED = 'UC'
    STATUS_ACTIVE = 'AC'
    STATUS_DISABLED = 'DS'

    STATUS_CHOICES = (
        (STATUS_UNCONFIRMED, 'Unconfirmed'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DISABLED, 'Disabled')
    )
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    nickname = models.CharField(max_length=64)

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    login_token = models.CharField(max_length=64)

    channels = models.ManyToManyField('Channel')

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
    author = models.OneToOneField('User')

    content = models.TextField()

    likers = models.ManyToManyField('User', related_name="liked_comments")
    dislikers = models.ManyToManyField('User', related_name="disliked_comments")