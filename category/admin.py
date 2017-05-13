from django.contrib import admin

from .models import *


# Register your models here.
class CategoryDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "image", "modified", "created"]


# list_display=["category_id","category_name"]

admin.site.register(CategoryData, CategoryDataAdmin)

# Register your models here.
