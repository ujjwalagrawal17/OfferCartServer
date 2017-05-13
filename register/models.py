from __future__ import unicode_literals

from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=120, primary_key=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    wallet = models.IntegerField(default=0)

    def __unicode__(self):
        return self.mobile
