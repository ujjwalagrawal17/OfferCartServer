from __future__ import unicode_literals

from django.db import models

from register.models import UserData


class CityData(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return str(self.name)


class CityFcmData(models.Model):
    user_id = models.ForeignKey(UserData, db_column="UserData.mobile")
    city_id = models.ForeignKey(CityData, db_column="CityData.id")
    fcm = models.CharField(max_length=512, blank=True, null=True)

    def __unicode__(self):
        return str(self.city_id)

        # def save(self, *args, **kwargs):
        # 	self.city_id = self.city_name.id
        # 	#self.user_id = self.user_mobile.mobile
        # 	super(city_fcm_data,self).save(*args, **kwargs)


class UserCityData(models.Model):
    user_id = models.ForeignKey(UserData, db_column="UserData.mobile")
    city_id = models.ForeignKey(CityData, db_column="CityData.id")
