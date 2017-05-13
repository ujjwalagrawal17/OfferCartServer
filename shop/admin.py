from django.contrib import admin

from .models import *


# Register your models here.
class ShopDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city_id", "category_id", "image",
                    "description", "modified", "created"]


admin.site.register(ShopData, ShopDataAdmin)

# Register your models here.
