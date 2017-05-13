from __future__ import unicode_literals

from django.db import models


# Create your models here.
class PaymentData(models.Model):
    transaction_id = models.CharField(max_length=15, blank=False, null=False)
    mobile = models.CharField(max_length=12, blank=False, null=False)
    amount = models.CharField(max_length=10, blank=True, null=False)
    transaction_type = models.CharField(max_length=10, blank=True, null=False)
    status = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
