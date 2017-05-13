from django.contrib import admin

from .models import *


class WelcomeDataAdmin(admin.ModelAdmin):
    list_display = ["id", "image_url", "message", "created", "modified"]


admin.site.register(WelcomeData, WelcomeDataAdmin)
# Register your models here.
