from __future__ import unicode_literals
from datetime import time
from django.db import models
from category.models import CategoryData
from city.models import CityData

def get_uplaod_file_name(userpic,filename):
    return u'photos/%s/%s_%s' % (str(userpic.user.id),str(time()).replace('.', '_'),filename)

class ShopData(models.Model):

    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    mobile = models.CharField(max_length=15,unique=True,blank=True,null=True)
    password = models.CharField(max_length=55, blank=False, null=False, default=0)
    description = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    category_id = models.ForeignKey(CategoryData, db_column="CategoryData.id")
    city_id = models.ForeignKey(CityData, db_column="CityData.id")
    image = models.ImageField(upload_to='shop/', default="/media/shop/default.png")
    verified = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return str(self.name)
        #
        # def save(self, *args, **kwargs):
        #     self.city_id = self.city_name.id
        #     self.category_id = self.category_name.id
        #     super(ShopData, self).save(*args, **kwargs)
