from __future__ import unicode_literals

from django.db import models


class WelcomeData(models.Model):
    image_url = models.ImageField(upload_to='welcome/', default="welcome/default.png")
    message = models.CharField(max_length=120, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
