from __future__ import unicode_literals

from django.db import models


# Create your models here.
class KeysData(models.Model):
    key = models.CharField(max_length=400, blank=True, null=True)
    value = models.CharField(max_length=400, blank=True, null=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    modified = models.DateTimeField(auto_now=False, auto_now_add=True)
