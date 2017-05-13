from django.contrib import admin

from .models import *


# Register your models here.
class CityDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "modified"]


admin.site.register(CityData, CityDataAdmin)


class UserCityDataAdmin(admin.ModelAdmin):
    list_display = ["id", "city_id", "user_id"]


admin.site.register(UserCityData, UserCityDataAdmin)


class CityFcmDataAdmin(admin.ModelAdmin):
    list_display = ["id", "city_id", "user_id"]


admin.site.register(CityFcmData, CityFcmDataAdmin)
