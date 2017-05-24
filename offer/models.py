from __future__ import unicode_literals

import datetime

from django.db import models

from shop.models import ShopData


class OfferData(models.Model):
    shop_id = models.ForeignKey(ShopData, db_column="ShopData.shop_id")

    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='offer/', default="/media/offer/default.png")
    active = models.BooleanField(default=False)
    expiry_date = models.DateField(default=datetime.date.today())
    validity = models.CharField(max_length=200, blank=True, null=True)
    offer_code = models.CharField(max_length=500, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    #
    # def save(self, *args, **kwargs):
    #     self.shop_id = self.shop_name.id
    #     super(OfferData, self).save(*args, **kwargs)


class OfferBoughtData(models.Model):
    mobile = models.CharField(max_length=120, blank=True, null=True)
    offer_id = models.IntegerField(default=-1)
    offer_code = models.CharField(max_length=20, blank=True, null=False)
    price = models.IntegerField(default=-1)
    avialable = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
