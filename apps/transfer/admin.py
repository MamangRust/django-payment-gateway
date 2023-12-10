from django.contrib import admin
from .models import Transfer


class TransferAdmin(admin.ModelAdmin):
    list_display = ("transfer_from", "transfer_to", "transfer_amount", "transfer_time")


admin.site.register(Transfer, TransferAdmin)
