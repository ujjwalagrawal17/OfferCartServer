from __future__ import unicode_literals

from django.db import models


# Create your models here.
class CategoryData(models.Model):
    name = models.CharField(max_length=120, unique=True, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='category/', default="category/default.png")
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return str(self.name)
