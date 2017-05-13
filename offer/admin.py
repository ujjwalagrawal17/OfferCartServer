from django.contrib import admin

from .models import *


class OfferDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "active", "shop_id", "validity", "image", "description", "created",
                    "modified", "price"]


admin.site.register(OfferData, OfferDataAdmin)


class OfferBoughtDataAdmin(admin.ModelAdmin):
    list_display = ["id", "mobile", "offer_id", "avialable", "price", "created", "modified"]


admin.site.register(OfferBoughtData, OfferBoughtDataAdmin)
