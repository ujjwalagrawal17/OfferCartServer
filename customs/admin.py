from django.contrib import admin

from .models import *


class KeysDataAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "created", "modified"]


admin.site.register(KeysData, KeysDataAdmin)
# Register your models here.
