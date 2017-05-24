from django.contrib import admin

from .models import *


# Register your models here.
class ShopDataAdmin(admin.ModelAdmin):
    list_display = [ "name", "city_id", "category_id", "image",
                    "description", "modified", "created"]


admin.site.register(ShopData, ShopDataAdmin)


class ShopOtpDataAdmin(admin.ModelAdmin):
    list_display = ["shop_id","otp","flag"]


admin.site.register(ShopOtpData, ShopOtpDataAdmin)

