from __future__ import unicode_literals

from django.db import models


# Create your models here.
class OtpData(models.Model):
    mobile = models.CharField(max_length=120, default='7587485272', blank=True, null=True)
    otp = models.IntegerField(default=0, null=True)
    flag = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
