from django.contrib import admin

# Register your models here.
from shop_otp.models import ShopOtpData


class ShopOtpDataAdmin(admin.ModelAdmin):
    list_display = ["mobile", "otp", "flag", "created", "modified"]


admin.site.register(ShopOtpData, ShopOtpDataAdmin)
