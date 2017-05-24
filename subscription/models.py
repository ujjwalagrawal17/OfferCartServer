from __future__ import unicode_literals

from django.db import models

from shop.models import ShopData


class SubscriptionData(models.Model):
    subscription_name = models.CharField(max_length=255)
    subscription_price = models.PositiveIntegerField()
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)


class ShopSubscriptionData(models.Model):
    shop_id = models.ForeignKey(ShopData)
    subscription_id = models.ForeignKey(SubscriptionData)
    payment_status = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)