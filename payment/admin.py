from django.contrib import admin

from .models import *


# Register your models here.
class PaymentDataAdmin(admin.ModelAdmin):
    list_display = ["mobile", "amount", "transaction_id", "status", "created", "modified"]


admin.site.register(PaymentData, PaymentDataAdmin)
