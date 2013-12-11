from django.db import models
from django.core.urlresolvers import reverse
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
    subscribers = models.ManyToManyField('main.User', related_name="subscriptions")

    def get_absolute_url(self):
        return reverse("view_channel", kwargs={"slug": self.name}) 

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError('Name is to short (<2 Chars)')

        if not re.match(r'^[A-Za-z0-9_-]+$', self.name):
            raise ValidationError("Name must only contain letters, numbers, underscores and hyphens.")